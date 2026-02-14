@echo off
REM GhostDrop - Production Server using Waitress (Windows-friendly)

echo ============================================
echo Starting GhostDrop Production Server
echo ============================================
echo.

REM Check if waitress is installed
"C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe" -c "import waitress" 2>nul
if errorlevel 1 (
    echo Installing Waitress server...
    "C:\Users\n2005\file sharingwebapp\.venv\Scripts\pip.exe" install waitress
)

REM Set production environment
set FLASK_ENV=production
set DEBUG=False

REM Start server
echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop
echo.

"C:\Users\n2005\file sharingwebapp\.venv\Scripts\waitress-serve" --host=0.0.0.0 --port=5000 --threads=4 run:app

pause
