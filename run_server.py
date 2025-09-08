#!/usr/bin/env python3
"""
Simple script to run the FastAPI server
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Run the FastAPI server"""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Change to the script directory
    os.chdir(script_dir)
    
    print("🚀 Starting Shelf Product Identifier API Server")
    print("="*50)
    print("Server will be available at:")
    print("  - API: http://localhost:8000")
    print("  - Docs: http://localhost:8000/docs")
    print("  - Health: http://localhost:8000/health")
    print("="*50)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the server
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Set to True for development
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
