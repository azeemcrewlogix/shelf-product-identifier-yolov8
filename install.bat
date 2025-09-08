@echo off
echo Installing Shelf Product Identifier API Server...
echo ================================================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating necessary directories...
if not exist "models" mkdir models
if not exist "src" mkdir src

echo.
echo Setup completed!
echo.
echo Next steps:
echo 1. Copy your YOLO model (best.pt) to the models/ folder
echo 2. Copy your knowledge base data to data/knowledge_base/
echo 3. Run: python train_model.py
echo 4. Run: python run_server.py
echo.
pause
