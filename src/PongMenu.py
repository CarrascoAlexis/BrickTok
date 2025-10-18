"""PongMenu.py

Created on 2025-10-17

Pong game menu scene.
- Player count selection
- AI difficulty selection
- Start button to begin game

"""
__author__ = "carras_a"
__version__ = "1.0"


from .Menu import Menu
from .MenuButton import MenuButton


class PongMenu(Menu):
    def __init__(self):
        """Initialize the Pong game menu."""
        super().__init__()

        # Internal state
        self.player_counts = [1, 2]
        self.player_index = 0  # default 1 players
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.diff_index = 1

        # Buttons
        self.players_button = MenuButton("PLAYERS", f"Players: {self.player_counts[self.player_index]}")
        self.ai_button = MenuButton("AI", f"AI: {self.difficulties[self.diff_index]}")
        self.start_button = MenuButton("START_PONG", "Play")
        self.back_button = MenuButton("MAIN_MENU", "Back")

        # Add to scene
        self.add_object(self.players_button)
        self.add_object(self.ai_button)
        self.add_object(self.start_button)
        self.add_object(self.back_button)
