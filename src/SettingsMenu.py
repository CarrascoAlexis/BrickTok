"""SettingsMenu.py

Created on 2025-10-17

Settings menu with editable options:
- FPS Limit
- Sound ON/OFF
- Difficulty

"""
__author__ = "carras_a"
__version__ = "1.0"

from .Menu import Menu
from .MenuButton import MenuButton


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.type = "SettingsMenu"

        # Internal settings state
        self.fps_options = [30, 60, 120]
        self.fps_index = 1  # default 60
        self.sound_on = True
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.diff_index = 1

        # Buttons
        self.fps_button = MenuButton("FPS", f"FPS: {self.fps_options[self.fps_index]}")
        self.sound_button = MenuButton("SOUND", f"Sound: {'ON' if self.sound_on else 'OFF'}")
        self.diff_button = MenuButton("DIFFICULTY", f"Difficulty: {self.difficulties[self.diff_index]}")
        self.back_button = MenuButton("MAIN_MENU", "Back")

        # Add to scene in order
        self.add_object(self.fps_button)
        self.add_object(self.sound_button)
        self.add_object(self.diff_button)
        self.add_object(self.back_button)
