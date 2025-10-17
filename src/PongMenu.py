"""PongMenu.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


from .Menu import Menu
from .MenuButton import MenuButton


class PongMenu(Menu):
    def __init__(self):
        super().__init__()

        # Internal state
        self.player_counts = [1, 2]
        self.player_index = 0  # default 1 players
        self.difficulties = ["Easy", "Normal", "Hard"]
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

    def render(self, screen):
        try:
            buttons = [self.players_button, self.ai_button, self.start_button, self.back_button]
            bw, bh = buttons[0].rect.size
            sw, sh = screen.get_width(), screen.get_height()

            total_height = len(buttons) * bh + (len(buttons) - 1) * 16
            start_y = (sh - total_height) // 2

            for idx, btn in enumerate(buttons):
                x = (sw - bw) // 2
                y = start_y + idx * (bh + 16)
                btn.setPosition((x, y))
        except Exception:
            pass

        super().render(screen)
