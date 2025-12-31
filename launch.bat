@echo off
REM Launcher script for PNG to ICO Converter GUI

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://python.org
    echo ========================================
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo.
    echo Launching GUI application...
    python gui_wrapper.py
) else (
    echo.
    echo Virtual environment not found, launching with system Python...
    python gui_wrapper.py
)

REM If there was an error, pause so user can see the message
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Application failed to start
    echo.
    echo Please ensure all dependencies are installed.
    echo Run setup.bat to set up the environment.
    echo ========================================
    echo.
    pause
    exit /b 1
)
