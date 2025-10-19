"""GameOverScreen.py

Created on 2025-10-19

Game Over screen for Brick Breaker showing final score.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .MenuButton import MenuButton


class GameOverScreen(Scene):
    def __init__(self, score):
        """Initialize the game over screen.

        Args:
            score: Final score achieved in the game
        """
        super().__init__()
        self.score = score

        # Get screen dimensions
        try:
            screen = pygame.display.get_surface()
            if screen:
                self.screen_width = screen.get_width()
                self.screen_height = screen.get_height()
            else:
                self.screen_width = 800
                self.screen_height = 600
        except Exception:
            self.screen_width = 800
            self.screen_height = 600

        # Load fonts
        try:
            self.title_font = pygame.font.Font(None, 100)
            self.score_font = pygame.font.Font(None, 80)
            self.label_font = pygame.font.Font(None, 40)
        except Exception:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 100)
            self.score_font = pygame.font.Font(None, 80)
            self.label_font = pygame.font.Font(None, 40)

        # Create buttons using MenuButton
        self.play_again_button = MenuButton("PLAY_BRICK_GAME", "Rejouer")
        self.main_menu_button = MenuButton("MAIN_MENU", "Menu principal")

        # Add buttons to scene
        self.add_object(self.play_again_button)
        self.add_object(self.main_menu_button)

    def render(self, screen):
        """Render the game over screen."""
        # Fill background with dark color
        screen.fill((20, 20, 40))

        # Render "GAME OVER" text
        game_over_text = "GAME OVER"
        game_over_color = (220, 50, 50)
        game_over_surface = self.title_font.render(
            game_over_text, True, game_over_color)
        game_over_rect = game_over_surface.get_rect(
            center=(self.screen_width // 2, 150))
        screen.blit(game_over_surface, game_over_rect)

        # Render "SCORE" label
        score_label = "SCORE"
        label_surface = self.label_font.render(
            score_label, True, (200, 200, 200))
        label_rect = label_surface.get_rect(
            center=(self.screen_width // 2, 250))
        screen.blit(label_surface, label_rect)

        # Render final score
        score_text = str(self.score)
        score_surface = self.score_font.render(score_text, True, (255, 215, 0))
        score_rect = score_surface.get_rect(
            center=(self.screen_width // 2, 320))
        screen.blit(score_surface, score_rect)

        # Layout buttons
        try:
            buttons = [self.play_again_button, self.main_menu_button]
            bw, bh = buttons[0].rect.size

            button_spacing = 20
            start_y = self.screen_height // 2 + 100

            for idx, btn in enumerate(buttons):
                x = (self.screen_width - bw) // 2
                y = start_y + idx * (bh + button_spacing)
                btn.setPosition((x, y))
                btn.rect.topleft = (x, y)
        except Exception:
            pass

        # Render all objects (buttons)
        super().render(screen)

    def update(self):
        """Update the game over screen."""
        # Update all buttons
        result = super().update()

        # Handle button clicks
        if result == "PLAY_BRICK_GAME":
            return "PLAY_BRICK_GAME"
        elif result == "MAIN_MENU":
            return "MAIN_MENU"

        return None
