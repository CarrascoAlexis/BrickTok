"""MainMenu.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame

from .Menu import Menu
from .MenuButton import MenuButton

class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        # Create the main menu buttons
        self.play_pong_button = MenuButton("PLAY_PONG", "Pong")
        self.play_brick_button = MenuButton("PLAY_BRICK", "Brick Breaker")
        self.settings_button = MenuButton("SETTINGS", "Settings")
        self.exit_button = MenuButton("EXIT", "Quitter")

        # Add them to the scene in the desired draw order
        self.add_object(self.play_pong_button)
        self.add_object(self.play_brick_button)
        self.add_object(self.settings_button)
        self.add_object(self.exit_button)

    def render(self, screen):
        # Layout buttons vertically centered with even spacing
        try:
            buttons = [self.play_pong_button, self.play_brick_button, self.settings_button, self.exit_button]
            # Get button sizes (assume uniform width/height)
            bw, bh = buttons[0].rect.size
            sw, sh = screen.get_width(), screen.get_height()

            total_height = len(buttons) * bh + (len(buttons) - 1) * 20  # 20 px spacing
            start_y = (sh - total_height) // 2

            for idx, btn in enumerate(buttons):
                x = (sw - bw) // 2
                y = start_y + idx * (bh + 20)
                btn.setPosition((x, y))
        except Exception:
            # If any error occurs (e.g. rect not yet initialized), continue and let rendering happen
            pass

        # Call parent render to draw all objects
        super().render(screen)