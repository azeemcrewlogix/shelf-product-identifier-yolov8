"""
Test script for the FastAPI server
"""

import requests
import json
import time

def test_api():
    """Test the FastAPI server endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Shelf Product Identifier API")
    print("="*50)
    
    # Test 1: Health check
    print("1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Model info
    print("\n2️⃣ Testing model info...")
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            print("✅ Model info retrieved")
            print(f"   Classes: {response.json()['knowledge_base_classes']}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model info error: {e}")
    
    # Test 3: Image upload (you need to provide an image file)
    print("\n3️⃣ Testing image upload...")
    print("   Note: You need to provide a shelf image file for this test")
    
    # Example with a test image (uncomment and modify path as needed)
    # test_image_path = "../data/img/testing.jpg"
    # if os.path.exists(test_image_path):
    #     try:
    #         with open(test_image_path, "rb") as f:
    #             files = {"file": ("test.jpg", f, "image/jpeg")}
    #             response = requests.post(f"{base_url}/detect-products", files=files)
    #         
    #         if response.status_code == 200:
    #             result = response.json()
    #             print("✅ Image processing successful")
    #             print(f"   Products detected: {result['total_products']}")
    #             for product in result['products'][:5]:  # Show first 5
    #                 print(f"   - {product['product_name']} ({product['confidence_percentage']}%)")
    #         else:
    #             print(f"❌ Image processing failed: {response.status_code}")
    #             print(f"   Error: {response.text}")
    #     except Exception as e:
    #         print(f"❌ Image processing error: {e}")
    # else:
    #     print("   ⚠️  Test image not found. Skipping image upload test.")
    
    print("\n" + "="*50)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    test_api()
