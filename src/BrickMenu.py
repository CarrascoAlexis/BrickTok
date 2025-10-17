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
    
    def render(self, screen):
        # Layout buttons vertically centered
        try:
            buttons = [self.players_button, self.play_button, self.back_button]
            bw, bh = buttons[0].rect.size
            sw, sh = screen.get_width(), screen.get_height()
            
            # Calculate total height with spacing
            total_height = len(buttons) * bh + (len(buttons) - 1) * 16
            start_y = (sh - total_height) // 2
            
            # Position each button
            for idx, btn in enumerate(buttons):
                x = (sw - bw) // 2
                y = start_y + idx * (bh + 16)
                btn.setPosition((x, y))
        except Exception:
            pass
        
        # Call parent render
        super().render(screen)
