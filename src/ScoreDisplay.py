"""ScoreDisplay.py

Created on 2025-10-18

Displays the score at the top center of the screen as a GameObject.
"""
__author__ = "carras_a"
__version__ = "1.0"

import pygame
from .GameObject import GameObject


class ScoreDisplay(GameObject):
    def __init__(self, p1_score_ref, p2_score_ref):
        """
        Initialize the score display.
        
        Args:
            p1_score_ref: Reference to player 1's score variable
            p2_score_ref: Reference to player 2's score variable
        """
        super().__init__()
        self.p1_score_ref = p1_score_ref
        self.p2_score_ref = p2_score_ref
        self.font = pygame.font.Font(None, 48)
        
    def update(self):
        """No update logic needed for score display."""
        return None
    
    def render(self, screen):
        """Render the combined score at top-center."""
        if screen:
            # Get current scores (using callable if they're functions/lambdas)
            p1_score = self.p1_score_ref() if callable(self.p1_score_ref) else self.p1_score_ref
            p2_score = self.p2_score_ref() if callable(self.p2_score_ref) else self.p2_score_ref
            
            score_text = f"P1 {p1_score}  -  {p2_score} P2"
            score_surf = self.font.render(score_text, True, (255, 255, 255))
            score_rect = score_surf.get_rect(midtop=(screen.get_width() // 2, 10))
            screen.blit(score_surf, score_rect)
