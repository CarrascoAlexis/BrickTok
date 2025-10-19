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
    def __init__(self, settings=None):
        super().__init__(title="SETTINGS")
        self.type = "SettingsMenu"

        # Internal settings state
        self.fps_options = [30, 60, 120, 240]
        self.fps_index = self.fps_options.index(settings[0]) if settings else 1 
        self.sound_on = settings[1] if settings else True
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.diff_index = 1

        # Buttons
        self.fps_button = MenuButton("FPS", f"FPS: {self.fps_options[self.fps_index]}")
        self.sound_button = MenuButton("SOUND", f"Sound: {'ON' if self.sound_on else 'OFF'}")
        self.back_button = MenuButton("MAIN_MENU", "Back")

        # Add to scene in order
        self.add_object(self.fps_button)
        self.add_object(self.sound_button)
        self.add_object(self.back_button)

    def update(self):
        """Update button labels and handle cycling on click."""
        # Update button labels
        self.fps_button.set_label(f"FPS: {self.fps_options[self.fps_index]}")
        self.sound_button.set_label(f"Sound: {'ON' if self.sound_on else 'OFF'}")
        
        # Check for button clicks before calling super().update()
        # This allows us to intercept the click and cycle the value
        result = None
        
        # Check FPS button click
        if self.fps_button.update() == "FPS":
            # Cycle to next FPS option
            self.fps_index = (self.fps_index + 1) % len(self.fps_options)
        # Check Sound button click
        elif self.sound_button.update() == "SOUND":
            # Toggle sound
            self.sound_on = not self.sound_on
            return "SOUND_TOGGLE"
        else:
            # Check back button (and any other objects)
            for obj in self.renderable_objects:
                if obj != self.fps_button and obj != self.sound_button:
                    obj_result = obj.update()
                    if obj_result:
                        result = obj_result
                        break
        super().update()
        return result