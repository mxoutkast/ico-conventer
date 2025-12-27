@echo off
REM Setup script for PNG to ICO Converter

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo.
echo To use the converter:
echo   1. Activate venv: venv\Scripts\activate
echo   2. Run: python ico_converter.py [options]
echo.
echo Example: python ico_converter.py image.png
echo ========================================
