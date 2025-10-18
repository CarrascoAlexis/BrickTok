"""BrickMenu.py

Created on 2025-10-17

Menu for Brick Breaker game setup
- Player count selection
- Play button to start
- Back button to return to main menu

"""
__author__ = "carras_a"
__version__ = "1.0"


from .Menu import Menu
from .MenuButton import MenuButton


class BrickMenu(Menu):
    def __init__(self):
        super().__init__()
        
        # Internal state
        self.player_counts = [1, 2]
        self.player_index = 0  # default 1 player
        
        # Create buttons
        self.players_button = MenuButton("PLAYERS", f"Players: {self.player_counts[self.player_index]}")
        self.play_button = MenuButton("PLAY_BRICK_GAME", "Play!")
        self.back_button = MenuButton("MAIN_MENU", "Back")
        
        # Add buttons to scene in order
        self.add_object(self.players_button)
        self.add_object(self.play_button)
        self.add_object(self.back_button)
