"""ScoreScreen.py

Created on 2025-10-18

End game screen showing which player won.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .MenuButton import MenuButton


class ScoreScreen(Scene):
    def __init__(self, winner, p1_score, p2_score):
        """Initialize the score screen.
        
        Args:
            winner: "P1" or "P2" indicating which player won
            p1_score: Final score for player 1
            p2_score: Final score for player 2
        """
        super().__init__()
        self.winner = winner
        self.p1_score = p1_score
        self.p2_score = p2_score
        
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
            self.score_font = pygame.font.Font(None, 60)
            self.info_font = pygame.font.Font(None, 36)
        except Exception:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 100)
            self.score_font = pygame.font.Font(None, 60)
            self.info_font = pygame.font.Font(None, 36)
        
        # Create buttons using MenuButton properly
        self.play_again_button = MenuButton("PLAY_PONG", "Rejouer")
        self.main_menu_button = MenuButton("MAIN_MENU", "Menu principal")
        
        # Add buttons to scene
        self.add_object(self.play_again_button)
        self.add_object(self.main_menu_button)
    
    def render(self, screen):
        """Render the score screen."""
        # Fill background with dark color
        screen.fill((20, 20, 40))
        
        # Render winner text
        winner_text = f"PLAYER {self.winner[1]} WINS!"  # Extract number from "P1" or "P2"
        winner_color = (255, 215, 0) if self.winner == "P1" else (255, 100, 100)
        winner_surface = self.title_font.render(winner_text, True, winner_color)
        winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(winner_surface, winner_rect)
        
        # Render final scores
        score_text = f"{self.p1_score}  -  {self.p2_score}"
        score_surface = self.score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(score_surface, score_rect)
        
        # Render player labels
        p1_label = self.info_font.render("Player 1", True, (200, 200, 200))
        p2_label = self.info_font.render("Player 2", True, (200, 200, 200))
        
        p1_rect = p1_label.get_rect(center=(self.screen_width // 2 - 100, 300))
        p2_rect = p2_label.get_rect(center=(self.screen_width // 2 + 100, 300))
        
        screen.blit(p1_label, p1_rect)
        screen.blit(p2_label, p2_rect)
        
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
        
        # Render buttons
        super().render(screen)
    
    def handle_event(self, event):
        """Handle keyboard events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        # Forward events to buttons
        super().handle_event(event)
