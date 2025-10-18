# BrickTok - Quick Start Script
# Run this to activate venv and start the game

Write-Host "🎮 BrickTok - Starting..." -ForegroundColor Cyan

# Check if .venv exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: py -3.13 -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Define venv python paths
$venvPython = ".\.venv\Scripts\python.exe"
$venvPip = ".\.venv\Scripts\pip.exe"

# Check if pygame is installed
Write-Host "✓ Checking dependencies..." -ForegroundColor Green
$pygame = & $venvPython -c "import pygame; print('installed')" 2>$null
if ($pygame -ne "installed") {
    Write-Host "⚠ Installing dependencies..." -ForegroundColor Yellow
    & $venvPip install -r requirements.txt
}

# Run the game using venv's python directly
Write-Host "✓ Starting game..." -ForegroundColor Green
& $venvPython main.py
