"""
Check if the standalone server setup is complete
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Check if all required files and directories exist"""
    
    print("🔍 Checking Shelf Product Identifier API Setup")
    print("="*50)
    
    issues = []
    warnings = []
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        issues.append(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}")
    else:
        print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check required directories
    required_dirs = ["models", "src", "data"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory exists: {dir_name}/")
        else:
            issues.append(f"Missing directory: {dir_name}/")
    
    # Check required files
    required_files = [
        "app.py",
        "train_model.py", 
        "run_server.py",
        "requirements.txt",
        "src/__init__.py",
        "src/img2vec_resnet18.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            issues.append(f"Missing file: {file_path}")
    
    # Check YOLO model
    yolo_model = "models/best.pt"
    if os.path.exists(yolo_model):
        size_mb = os.path.getsize(yolo_model) / (1024 * 1024)
        print(f"✅ YOLO model: {yolo_model} ({size_mb:.1f} MB)")
    else:
        issues.append(f"Missing YOLO model: {yolo_model}")
    
    # Check knowledge base
    kb_path = "data/knowledge_base/crops/object"
    if os.path.exists(kb_path):
        kb_images = len([f for f in os.listdir(kb_path) if f.endswith('.jpg')])
        print(f"✅ Knowledge base: {kb_path} ({kb_images} images)")
    else:
        issues.append(f"Missing knowledge base: {kb_path}")
    
    # Check trained k-NN model
    knn_model = "models/knn_model.pkl"
    if os.path.exists(knn_model):
        size_mb = os.path.getsize(knn_model) / (1024 * 1024)
        print(f"✅ Trained k-NN model: {knn_model} ({size_mb:.1f} MB)")
    else:
        warnings.append(f"k-NN model not trained: {knn_model} (run python train_model.py)")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    try:
        import fastapi
        print("✅ FastAPI installed")
    except ImportError:
        issues.append("FastAPI not installed (run: pip install -r requirements.txt)")
    
    try:
        import ultralytics
        print("✅ Ultralytics installed")
    except ImportError:
        issues.append("Ultralytics not installed (run: pip install -r requirements.txt)")
    
    try:
        import torch
        print("✅ PyTorch installed")
    except ImportError:
        issues.append("PyTorch not installed (run: pip install -r requirements.txt)")
    
    try:
        import sklearn
        print("✅ Scikit-learn installed")
    except ImportError:
        issues.append("Scikit-learn not installed (run: pip install -r requirements.txt)")
    
    # Summary
    print("\n" + "="*50)
    if issues:
        print("❌ SETUP ISSUES FOUND:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n🔧 Fix these issues before running the server")
    else:
        print("✅ SETUP LOOKS GOOD!")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not issues:
        print("\n🚀 Ready to start the server!")
        print("   Run: python run_server.py")
    
    print("="*50)
    
    return len(issues) == 0

if __name__ == "__main__":
    success = check_setup()
    sys.exit(0 if success else 1)
