"""
Script to train and save the k-NN model for faster inference
Run this once to pre-train the model, then the FastAPI server will load it
"""

import os
import glob
import joblib
import numpy as np
from pathlib import Path
from src.img2vec_resnet18 import Img2VecResnet18
from sklearn.neighbors import NearestNeighbors
from collections import Counter
import time

def train_knn_model():
    """Train k-NN model on knowledge base and save it"""
    
    print("🚀 Starting k-NN model training...")
    start_time = time.time()
    
    # Configuration
    DATA_PATH = '../data'
    MODEL_PATH = 'models'
    N_NEIGHBORS = 5
    
    # Create models directory if it doesn't exist
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    # Get knowledge base images
    print("📚 Loading knowledge base images...")
    list_imgs = glob.glob(f"{DATA_PATH}/knowledge_base/crops/object/**/*.jpg")
    print(f"Found {len(list_imgs)} training images")
    
    if len(list_imgs) == 0:
        raise ValueError("No training images found in knowledge base!")
    
    # Initialize feature extractor
    print("🧠 Initializing ResNet18 feature extractor...")
    img2vec = Img2VecResnet18()
    
    # Extract features and classes
    print("🔄 Extracting features from training images...")
    classes = []
    embeddings = []
    
    for i, filename in enumerate(list_imgs):
        if i % 10 == 0:
            print(f"   Processing image {i+1}/{len(list_imgs)}")
        
        try:
            from PIL import Image
            img = Image.open(filename)
            features = img2vec.getVec(img)
            img.close()
            
            # Extract class from folder name
            folder_name = os.path.basename(os.path.dirname(filename))
            classes.append(folder_name)
            embeddings.append(features)
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            continue
    
    print(f"✅ Successfully processed {len(embeddings)} images")
    
    # Convert to numpy arrays
    embeddings = np.array(embeddings)
    classes = np.array(classes)
    
    # Train k-NN model
    print("🎯 Training k-NN classifier...")
    knn_start = time.time()
    
    knn_model = NearestNeighbors(metric='cosine', n_neighbors=N_NEIGHBORS)
    knn_model.fit(embeddings)
    
    knn_time = time.time() - knn_start
    print(f"✅ k-NN training completed in {knn_time:.2f}s")
    
    # Save the model
    print("💾 Saving trained model...")
    model_data = {
        'knn_model': knn_model,
        'classes': classes,
        'embeddings': embeddings,
        'n_neighbors': N_NEIGHBORS,
        'training_time': time.time() - start_time,
        'num_training_samples': len(embeddings)
    }
    
    model_file = os.path.join(MODEL_PATH, 'knn_model.pkl')
    joblib.dump(model_data, model_file)
    
    # Print summary
    total_time = time.time() - start_time
    print("\n" + "="*50)
    print("📊 TRAINING SUMMARY")
    print("="*50)
    print(f"⏱️  Total training time: {total_time:.2f}s")
    print(f"📚 Training samples: {len(embeddings)}")
    print(f"🏷️  Classes: {len(set(classes))}")
    print(f"📁 Model saved to: {model_file}")
    print(f"📦 Model size: {os.path.getsize(model_file) / 1024 / 1024:.2f} MB")
    
    # Show class distribution
    class_counts = Counter(classes)
    print(f"\n📈 Class distribution:")
    for class_name, count in class_counts.most_common():
        print(f"   {class_name}: {count} images")
    
    print("="*50)
    print("🎉 Model training completed successfully!")
    print("You can now start the FastAPI server with: python app.py")
    
    return model_file

if __name__ == "__main__":
    try:
        train_knn_model()
    except Exception as e:
        print(f"❌ Training failed: {e}")
        exit(1)
