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
        super().__init__(title="BRICKTOK")
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
