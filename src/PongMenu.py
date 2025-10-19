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
        super().__init__(title="PONG")

        # Internal state
        self.player_counts = [1, 2]
        self.player_index = 0  # default 1 players
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.diff_index = 1

        # Buttons
        self.players_button = MenuButton(
            "PLAYERS", f"Players: {self.player_counts[self.player_index]}")
        self.ai_button = MenuButton(
            "AI", f"AI: {self.difficulties[self.diff_index]}")
        self.start_button = MenuButton("START_PONG", "Play")
        self.back_button = MenuButton("MAIN_MENU", "Back")

        # Add to scene
        self.add_object(self.players_button)
        self.add_object(self.ai_button)
        self.add_object(self.start_button)
        self.add_object(self.back_button)

    def update(self):
        """Update button labels and handle cycling on click."""
        # Update button labels
        self.players_button.set_label(
            f"Players: {self.player_counts[self.player_index]}")
        self.ai_button.set_label(f"AI: {self.difficulties[self.diff_index]}")
        # Check for button clicks before calling super().update()
        # This allows us to intercept the click and cycle the value
        # Check Players button click
        if self.players_button.update() == "PLAYERS":
            # Cycle to next player count
            self.player_index = (self.player_index +
                                 1) % len(self.player_counts)

        # Check AI button click
        elif self.ai_button.update() == "AI":
            # Cycle to next difficulty
            self.diff_index = (self.diff_index + 1) % len(self.difficulties)

        # Check Start button click
        elif self.start_button.update() == "START_PONG":
            return ("START_PONG",
                    self.player_counts[self.player_index],
                    self.difficulties[self.diff_index])

        return super().update()
