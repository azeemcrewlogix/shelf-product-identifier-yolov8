from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import shutil
from pathlib import Path
import time
import json
from typing import List, Dict
import numpy as np
from ultralytics import YOLO
from src.img2vec_resnet18 import Img2VecResnet18
from sklearn.neighbors import NearestNeighbors
from collections import Counter
import joblib
import glob

app = FastAPI(title="Shelf Product Identifier API", version="1.0.0")

# Global variables for models
yolo_model = None
img2vec_model = None
knn_model = None
classes = None
embeddings = None

class ProductDetector:
    def __init__(self):
        self.yolo_model = None
        self.img2vec_model = None
        self.knn_model = None
        self.classes = None
        self.embeddings = None
        self.model_loaded = False
    
    def load_models(self):
        """Load all pre-trained models"""
        try:
            print("🔄 Loading models...")
            
            # Load YOLO model
            self.yolo_model = YOLO('models/best.pt')
            print("✅ YOLO model loaded")
            
            # Load image feature extractor
            self.img2vec_model = Img2VecResnet18()
            print("✅ ResNet18 feature extractor loaded")
            
            # Load pre-trained k-NN model
            if os.path.exists('models/knn_model.pkl'):
                model_data = joblib.load('models/knn_model.pkl')
                self.knn_model = model_data['knn_model']
                self.classes = model_data['classes']
                self.embeddings = model_data['embeddings']
                print("✅ Pre-trained k-NN model loaded")
            else:
                print("❌ Pre-trained k-NN model not found. Please run train_model.py first.")
                return False
            
            self.model_loaded = True
            print("🎉 All models loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {str(e)}")
            return False
    
    def detect_products(self, image_path: str) -> List[Dict]:
        """Detect and classify products in a shelf image"""
        if not self.model_loaded:
            raise HTTPException(status_code=500, detail="Models not loaded")
        
        start_time = time.time()
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Step 1: YOLO Object Detection
            print("🔍 Running YOLO detection...")
            yolo_start = time.time()
            
            results = self.yolo_model.predict(
                source=image_path,
                save=True,
                save_crop=True,
                conf=0.5,
                project=str(temp_path),
                name="detection",
                exist_ok=True
            )
            
            yolo_time = time.time() - yolo_start
            print(f"✅ YOLO detection completed in {yolo_time:.2f}s")
            
            # Step 2: Find cropped images
            crop_dir = temp_path / "detection" / "crops" / "object"
            if not crop_dir.exists():
                return []
            
            crop_images = list(crop_dir.glob("*.jpg"))
            print(f"📦 Found {len(crop_images)} products to classify")
            
            # Step 3: Classify each product
            products = []
            classification_start = time.time()
            
            for i, crop_path in enumerate(crop_images):
                try:
                    # Extract features
                    from PIL import Image
                    img = Image.open(crop_path)
                    features = self.img2vec_model.getVec(img)
                    img.close()
                    
                    # Find nearest neighbors
                    distances, indices = self.knn_model.kneighbors([features])
                    
                    # Get class labels of nearest neighbors
                    neighbor_classes = [self.classes[idx] for idx in indices[0]]
                    
                    # Count occurrences
                    class_counts = Counter(neighbor_classes)
                    
                    # Get most common class and confidence
                    most_common_class, count = class_counts.most_common(1)[0]
                    confidence = count / 5.0  # 5 neighbors
                    
                    # Create product info
                    product_info = {
                        "crop_id": crop_path.stem,
                        "product_name": most_common_class,
                        "confidence": round(confidence, 3),
                        "confidence_percentage": round(confidence * 100, 1)
                    }
                    
                    products.append(product_info)
                    
                except Exception as e:
                    print(f"❌ Error processing {crop_path}: {str(e)}")
                    continue
            
            classification_time = time.time() - classification_start
            total_time = time.time() - start_time
            
            print(f"✅ Classification completed in {classification_time:.2f}s")
            print(f"⏱️ Total processing time: {total_time:.2f}s")
            
            return products

# Initialize detector
detector = ProductDetector()

@app.on_event("startup")
async def startup_event():
    """Load models when the server starts"""
    success = detector.load_models()
    if not success:
        print("⚠️ Warning: Some models failed to load. Check the logs.")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Shelf Product Identifier API",
        "status": "running",
        "models_loaded": detector.model_loaded
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if detector.model_loaded else "unhealthy",
        "models_loaded": detector.model_loaded,
        "yolo_loaded": detector.yolo_model is not None,
        "img2vec_loaded": detector.img2vec_model is not None,
        "knn_loaded": detector.knn_model is not None
    }

@app.post("/detect-products")
async def detect_products(file: UploadFile = File(...)):
    """
    Detect and classify products in a shelf image
    
    Returns:
    - List of detected products with names and confidence scores
    """
    if not detector.model_loaded:
        raise HTTPException(status_code=500, detail="Models not loaded. Please check server logs.")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Process the image
        products = detector.detect_products(tmp_path)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        # Prepare response
        response = {
            "success": True,
            "total_products": len(products),
            "products": products,
            "processing_info": {
                "input_filename": file.filename,
                "timestamp": time.time()
            }
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about loaded models"""
    return {
        "yolo_model": "YOLOv8 (best.pt)" if detector.yolo_model else None,
        "feature_extractor": "ResNet18" if detector.img2vec_model else None,
        "classifier": "k-NN" if detector.knn_model else None,
        "knowledge_base_classes": detector.classes if detector.classes else [],
        "knowledge_base_size": len(detector.classes) if detector.classes else 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
