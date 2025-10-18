# BrickTok - Setup Guide

A Pong game built with Python and Pygame.

## Requirements

- Python 3.13 (recommended)
- Windows 10/11

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CarrascoAlexis/BrickTok.git
cd BrickTok
```

### 2. Create virtual environment

**Using Python 3.13 (recommended):**
```powershell
py -3.13 -m venv .venv
```

**Or using default Python:**
```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## Running the Game

```powershell
python main.py
```

## Controls

### Main Menu
- **Mouse**: Click buttons
- **Keyboard**: Arrow keys or W/S to navigate, Enter/Space to select

### Pong Game
- **Player 1**: Arrow keys (↑/↓)
- **Player 2**: W/S keys
- **Pause**: P key
- **Launch ball**: Spacebar
- **Return to menu**: Escape

### Global
- **Toggle fullscreen**: F11 or Escape (from game)
- **Show FPS**: F3

## Features

- ✅ Single player vs AI (Easy/Medium/Hard difficulty)
- ✅ Two player local multiplayer
- ✅ Progressive ball speed increase
- ✅ Angle-based paddle bounces
- ✅ AI with difficulty-based behavior
- ✅ Sound effects
- ✅ Fullscreen and windowed mode
- ✅ FPS display

## Development

### Project Structure

```
BrickTok/
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── src/                 # Source code
│   ├── game.py         # Game loop manager
│   ├── Ball.py         # Ball physics
│   ├── Raquette.py     # Paddle (player/AI)
│   ├── PongLevel.py    # Pong game scene
│   ├── Menu.py         # Menu base class
│   └── ...             # Other components
├── assets/             # Game assets
│   ├── images/        # Sprites and images
│   ├── sounds/        # Sound effects
│   └── fonts/         # Custom fonts
└── levels/            # Level definitions
```

## Troubleshooting

### Import errors with pkg_resources

This is a harmless warning from pygame itself. To suppress it:
```powershell
pip install --upgrade setuptools
```

### Python 3.14 compatibility

Pygame 2.6.1 doesn't support Python 3.14 yet. Use Python 3.13:
```powershell
py -3.13 -m venv .venv
```

### Virtual environment not activating

Check your PowerShell execution policy:
```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## License

Project created for ETNA POOL (2nd week bonus project)

## Author

**carras_a**
- Version: 1.0
- Created: October 2025
