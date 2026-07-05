@echo off
REM GhostDrop - Start as Background Process

echo Starting GhostDrop in background...

REM Set environment
set FLASK_ENV=production

REM Kill any existing instance
taskkill /F /IM python.exe /FI "WINDOWTITLE eq GhostDrop*" >nul 2>&1

REM Start in background (detached)
start "GhostDrop" /B "C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe" run.py

echo.
echo ============================================
echo GhostDrop started in background!
echo ============================================
echo.
echo Running on: http://localhost:5000
echo.
echo To stop: run stop_ghostdrop.bat
echo Or use: taskkill /F /IM python.exe
echo.

pause
