# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- YOLO model file (`best.pt`)
- Knowledge base images

### Step 1: Install Dependencies

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Manual:**
```bash
pip install -r requirements.txt
```

### Step 2: Add Required Files

Copy these files to the standalone_server folder:

1. **YOLO Model:**
   ```
   Copy: ../models/best.pt
   To:   models/best.pt
   ```

2. **Knowledge Base:**
   ```
   Copy: ../data/knowledge_base/
   To:   data/knowledge_base/
   ```

### Step 3: Train the Model

```bash
python train_model.py
```

This creates `models/knn_model.pkl` (one-time setup).

### Step 4: Start the Server

```bash
python run_server.py
```

### Step 5: Test the API

Open another terminal:
```bash
python test_api.py
```

Or visit: http://localhost:8000/docs

## 📁 Required File Structure

```
standalone_server/
├── models/
│   └── best.pt              # YOLO model (copy from parent)
├── data/
│   └── knowledge_base/      # Training images (copy from parent)
│       └── crops/object/
├── src/
│   └── img2vec_resnet18.py  # ✅ Already included
├── app.py                   # ✅ Main server
├── train_model.py           # ✅ Model training
├── run_server.py            # ✅ Server runner
├── requirements.txt         # ✅ Dependencies
└── README.md               # ✅ Full documentation
```

## 🔧 Troubleshooting

### "No module named 'src'"
- Make sure you're in the standalone_server directory
- Check that `src/__init__.py` exists

### "YOLO model not found"
- Copy `best.pt` to `models/best.pt`
- Check file permissions

### "Knowledge base not found"
- Copy knowledge base to `data/knowledge_base/`
- Run `python train_model.py` first

### "Models not loaded"
- Run `python train_model.py` to create k-NN model
- Check that all model files exist

## 📞 API Usage

### Upload Image
```bash
curl -X POST "http://localhost:8000/detect-products" \
     -F "file=@your_shelf_image.jpg"
```

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Visit: http://localhost:8000/docs

## ⚡ Performance

- **First request**: ~15-20 seconds
- **Subsequent requests**: ~10-15 seconds
- **Memory usage**: ~2-4 GB
- **Concurrent requests**: Supported

## 🎯 What You Get

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
    }
  ]
}
```

Ready to go! 🚀
