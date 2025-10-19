# Script to build BrickTok executable
# Run this script to create a standalone .exe file

Write-Host "=== BrickTok Executable Builder ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
}

# Install PyInstaller if not already installed
Write-Host "Installing PyInstaller..." -ForegroundColor Green
pip install pyinstaller

Write-Host ""
Write-Host "Building executable..." -ForegroundColor Green
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
Write-Host ""

# Build the executable with PyInstaller
# --onefile: Create a single executable file
# --windowed: Hide console window (GUI app)
# --name: Name of the executable
# --icon: Icon file (if you have one)
# --add-data: Include assets folder
pyinstaller --onefile `
    --windowed `
    --name BrickTok `
    --add-data "assets;assets" `
    --add-data "levels;levels" `
    main.py

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Your executable is located at:" -ForegroundColor Yellow
Write-Host "  dist\BrickTok.exe" -ForegroundColor White
Write-Host ""
Write-Host "You can now:" -ForegroundColor Cyan
Write-Host "  1. Double-click dist\BrickTok.exe to run the game" -ForegroundColor White
Write-Host "  2. Copy the entire 'dist' folder to share your game" -ForegroundColor White
Write-Host "==================================" -ForegroundColor Cyan
