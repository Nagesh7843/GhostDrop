# GhostDrop - PowerShell Production Starter
# Run as: .\start_production.ps1

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Starting GhostDrop Production Server" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Set production environment
$env:FLASK_ENV = "production"
$env:DEBUG = "False"

# Install waitress if not present
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& "C:\Users\n2005\file sharingwebapp\.venv\Scripts\python.exe" -m pip install waitress --quiet

# Start server
Write-Host "`nStarting server on http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

& "C:\Users\n2005\file sharingwebapp\.venv\Scripts\waitress-serve" --host=0.0.0.0 --port=5000 --threads=4 run:app
