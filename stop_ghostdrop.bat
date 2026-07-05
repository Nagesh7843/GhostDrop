@echo off
REM GhostDrop - Stop Background Process

echo Stopping GhostDrop...

taskkill /F /IM python.exe /FI "WINDOWTITLE eq GhostDrop*"

echo.
echo GhostDrop stopped.
echo.

pause
