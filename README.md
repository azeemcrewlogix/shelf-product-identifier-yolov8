# Shelf Product Identifier API

A FastAPI-based server that detects and classifies products in shelf images using YOLO object detection and ResNet18 + k-NN classification.

## Features

- 🚀 **Fast API**: RESTful API for shelf image processing
- 🔍 **Object Detection**: YOLO-based product detection and cropping
- 🧠 **AI Classification**: ResNet18 feature extraction + k-NN classification
- ⚡ **Pre-trained Models**: Save time with pre-trained k-NN model
- 📊 **Confidence Scores**: Get accuracy percentages for each detection
- 🎯 **Multiple SKUs**: Detect and classify multiple products in one image

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the k-NN Model (One-time setup)

```bash
python train_model.py
```

This will:
- Process all images in the knowledge base
- Extract ResNet18 features
- Train k-NN classifier
- Save the model to `models/knn_model.pkl`

### 3. Start the Server

```bash
python app.py
```

The server will start at `http://localhost:8000`

### 4. Test the API

```bash
python test_api.py
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Model Information
```bash
GET /model-info
```

### Detect Products
```bash
POST /detect-products
Content-Type: multipart/form-data

# Upload a shelf image file
```

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Upload image and detect products
curl -X POST "http://localhost:8000/detect-products" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@shelf_image.jpg"
```

### Using Python requests

```python
import requests

# Upload image
with open("shelf_image.jpg", "rb") as f:
    files = {"file": ("shelf_image.jpg", f, "image/jpeg")}
    response = requests.post("http://localhost:8000/detect-products", files=files)

result = response.json()
print(f"Detected {result['total_products']} products:")
for product in result['products']:
    print(f"- {product['product_name']}: {product['confidence_percentage']}%")
```

## Response Format

```json
{
  "success": true,
  "total_products": 5,
  "products": [
    {
      "crop_id": "testing",
      "product_name": "cocacola_can",
      "confidence": 0.8,
      "confidence_percentage": 80.0
    },
    {
      "crop_id": "testing2",
      "product_name": "sprite_pet",
      "confidence": 0.6,
      "confidence_percentage": 60.0
    }
  ],
  "processing_info": {
    "input_filename": "shelf_image.jpg",
    "timestamp": 1694123456.789
  }
}
```

## Performance

- **Model Loading**: ~3-5 seconds on startup
- **Per Image Processing**: ~10-20 seconds for 50-100 products
- **Average per Product**: ~0.1-0.2 seconds
- **Memory Usage**: ~2-4 GB (depending on model size)

## File Structure

```
standalone_server/
├── app.py              # FastAPI server
├── train_model.py      # Model training script
├── test_api.py         # API testing script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── models/            # Model files (created after training)
│   ├── best.pt        # YOLO model (copy from parent)
│   └── knn_model.pkl  # Trained k-NN model
└── src/               # Source code (copy from parent)
    └── img2vec_resnet18.py
```

## Setup Instructions

1. **Copy required files**:
   ```bash
   # Copy YOLO model
   cp ../models/best.pt models/
   
   # Copy source code
   cp -r ../src ./
   ```

2. **Train the model**:
   ```bash
   python train_model.py
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```

## Troubleshooting

### Models not loading
- Ensure `models/best.pt` exists (YOLO model)
- Run `python train_model.py` to create k-NN model
- Check file permissions

### Memory issues
- Reduce batch size in processing
- Use smaller images
- Close other applications

### Slow performance
- Use GPU if available
- Reduce image resolution
- Pre-train k-NN model (already included)

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

Same as the parent project.
