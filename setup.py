"""
Complete setup script for the standalone server
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def setup_standalone_server():
    """Complete setup for the standalone server"""
    
    print("🚀 Setting up Shelf Product Identifier API Server")
    print("="*60)
    
    # Get current directory
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    # Create necessary directories
    print("📁 Creating directories...")
    os.makedirs("models", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    print("✅ Directories created")
    
    # Copy YOLO model
    print("📦 Copying YOLO model...")
    yolo_src = parent_dir / "models" / "best.pt"
    yolo_dst = current_dir / "models" / "best.pt"
    
    if yolo_src.exists():
        shutil.copy2(yolo_src, yolo_dst)
        size_mb = os.path.getsize(yolo_dst) / (1024 * 1024)
        print(f"✅ YOLO model copied ({size_mb:.1f} MB)")
    else:
        print("❌ YOLO model not found at ../models/best.pt")
        print("   Please copy best.pt to models/ folder manually")
        return False
    
    # Copy knowledge base
    print("📚 Copying knowledge base...")
    kb_src = parent_dir / "data" / "knowledge_base"
    kb_dst = current_dir / "data" / "knowledge_base"
    
    if kb_src.exists():
        if kb_dst.exists():
            shutil.rmtree(kb_dst)
        shutil.copytree(kb_src, kb_dst)
        
        # Count images
        kb_images = len(list(kb_dst.rglob("*.jpg")))
        print(f"✅ Knowledge base copied ({kb_images} images)")
    else:
        print("❌ Knowledge base not found at ../data/knowledge_base/")
        print("   Please copy knowledge base to data/ folder manually")
        return False
    
    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("   Try running: pip install -r requirements.txt")
        return False
    
    # Train the k-NN model
    print("🧠 Training k-NN model...")
    try:
        result = subprocess.run([sys.executable, "train_model.py"], 
                              capture_output=True, text=True, cwd=current_dir)
        if result.returncode == 0:
            print("✅ k-NN model trained and saved")
        else:
            print(f"❌ Failed to train k-NN model: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error training k-NN model: {e}")
        return False
    
    # Final verification
    print("🔍 Verifying setup...")
    try:
        result = subprocess.run([sys.executable, "check_setup.py"], 
                              capture_output=True, text=True, cwd=current_dir)
        if result.returncode == 0:
            print("✅ Setup verification passed")
        else:
            print("⚠️  Setup verification found issues:")
            print(result.stdout)
    except Exception as e:
        print(f"⚠️  Could not verify setup: {e}")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 What was set up:")
    print("   ✅ All required files copied")
    print("   ✅ Dependencies installed")
    print("   ✅ k-NN model trained")
    print("   ✅ Ready to run!")
    
    print("\n🚀 Next steps:")
    print("   1. Start server: python run_server.py")
    print("   2. Test API: python test_api.py")
    print("   3. API docs: http://localhost:8000/docs")
    
    print("\n📁 Your standalone server is ready!")
    print("   You can now copy this entire folder to any machine")
    print("   and it will work independently.")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = setup_standalone_server()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        print("\n🔧 Manual setup steps:")
        print("   1. Copy best.pt to models/")
        print("   2. Copy knowledge_base to data/")
        print("   3. Run: pip install -r requirements.txt")
        print("   4. Run: python train_model.py")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")