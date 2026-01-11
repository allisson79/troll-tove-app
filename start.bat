@echo off
REM Quick start script for local development on Windows

echo 🔮 Troll-Tove Local Development Setup
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python is installed and in your PATH
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    
    REM Generate a random SECRET_KEY
    for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i
    
    REM Update .env with generated key
    powershell -Command "(gc .env) -replace 'your-secret-key-here', '%SECRET_KEY%' | Out-File -encoding ASCII .env"
    
    REM Enable debug mode for local development
    powershell -Command "(gc .env) -replace 'FLASK_DEBUG=false', 'FLASK_DEBUG=true' | Out-File -encoding ASCII .env"
    
    echo ✓ .env file created with random SECRET_KEY
)

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

REM Run the application
echo.
echo Starting Troll-Tove app...
echo Access the app at: http://localhost:5000
echo Health check: http://localhost:5000/health
echo Press Ctrl+C to stop
echo.

python app.py
