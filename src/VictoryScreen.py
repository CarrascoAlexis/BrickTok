"""VictoryScreen.py

Created on 2025-10-19

Victory screen for Brick Breaker when completing a level.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .MenuButton import MenuButton


class VictoryScreen(Scene):
    def __init__(self, level_number, score, has_next_level=True):
        """Initialize the victory screen.
        
        Args:
            level_number: The level that was just completed
            score: Current score
            has_next_level: Whether there's a next level available
        """
        super().__init__()
        self.level_number = level_number
        self.score = score
        self.has_next_level = has_next_level
        
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
            self.info_font = pygame.font.Font(None, 40)
        except Exception:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 100)
            self.score_font = pygame.font.Font(None, 60)
            self.info_font = pygame.font.Font(None, 40)
        
        # Create buttons
        if has_next_level:
            self.next_button = MenuButton("NEXT_LEVEL", "Niveau suivant")
            self.add_object(self.next_button)
        
        self.menu_button = MenuButton("MAIN_MENU", "Menu principal")
        self.add_object(self.menu_button)
    
    def render(self, screen):
        """Render the victory screen."""
        # Fill background with dark color
        screen.fill((20, 30, 50))
        
        # Render "LEVEL COMPLETE" text
        victory_text = "LEVEL COMPLETE!"
        victory_color = (50, 255, 100)
        victory_surface = self.title_font.render(victory_text, True, victory_color)
        victory_rect = victory_surface.get_rect(center=(self.screen_width // 2, 120))
        screen.blit(victory_surface, victory_rect)
        
        # Render level number
        level_text = f"Level {self.level_number}"
        level_surface = self.info_font.render(level_text, True, (200, 200, 200))
        level_rect = level_surface.get_rect(center=(self.screen_width // 2, 220))
        screen.blit(level_surface, level_rect)
        
        # Render "SCORE" label
        score_label = "SCORE"
        label_surface = self.info_font.render(score_label, True, (200, 200, 200))
        label_rect = label_surface.get_rect(center=(self.screen_width // 2, 300))
        screen.blit(label_surface, label_rect)
        
        # Render score
        score_text = str(self.score)
        score_surface = self.score_font.render(score_text, True, (255, 215, 0))
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, 370))
        screen.blit(score_surface, score_rect)
        
        # Layout buttons
        try:
            buttons = []
            if self.has_next_level:
                buttons.append(self.next_button)
            buttons.append(self.menu_button)
            
            if buttons:
                bw, bh = buttons[0].rect.size
                button_spacing = 20
                start_y = self.screen_height // 2 + 150
                
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
        """Update the victory screen."""
        # Update all buttons
        result = super().update()
        
        # Handle button clicks
        if result == "NEXT_LEVEL":
            return "NEXT_LEVEL"
        elif result == "MAIN_MENU":
            return "MAIN_MENU"
        
        return None
