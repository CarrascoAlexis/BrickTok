"""PongLevel.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .Raquette import Raquette
from .Ball import Ball
from .ScoreDisplay import ScoreDisplay

class PongLevel(Scene):
    def __init__(self, players=2, difficulty="MEDIUM"):
        super().__init__()
        self.paused = False
        self.num_players = players
        self.ai_difficulty = difficulty.upper()
        
        # Create paddles and position them
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        # Left paddle - always player 1
        self.p1 = Raquette("P1")
        self.p1.rect.x = 50  # Fixed x position from left
        self.p1.rect.y = (screen_height - self.p1.rect.height) // 2
        
        # Right paddle - player 2 or AI depending on player count
        if players == 2:
            self.p2 = Raquette("P2")
        else:
            self.p2 = Raquette("IA", difficulty=self.ai_difficulty)
        self.p2.rect.x = screen_width - 50 - self.p2.rect.width  # Fixed x position from right
        self.p2.rect.y = (screen_height - self.p2.rect.height) // 2
        
        # Create and position ball
        self.ball = Ball()
        self.ball.reset()  # This will position the ball in the center
        
        # Set ball reference for AI paddles
        if self.p2.is_ai:
            self.p2.set_ball(self.ball)
        
        # Initialize scores
        self.p1_score = 0
        self.p2_score = 0
        self.winning_score = 10  # First to 10 wins
        
        # Create UI elements
        self.score_display = ScoreDisplay(
            lambda: self.p1_score,  # Pass lambdas to get current score values
            lambda: self.p2_score
        )
        
        # Add all objects to scene (order matters for rendering)
        self.add_object(self.p1)
        self.add_object(self.p2)
        self.add_object(self.ball)
        self.add_object(self.score_display)  # Draw score last (foreground)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
            elif event.key == pygame.K_p:
                self.paused = not self.paused
        
        # Only pass events to objects if not paused
        if not self.paused:
            super().handle_event(event)
    
    def update(self):
        # Handle pause state
        if self.paused:
            # Draw pause text
            font = pygame.font.Font(None, 74)
            screen = pygame.display.get_surface()
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(pause_text, pause_rect)
            return None
        
        # Handle ball collisions with paddles BEFORE updating positions
        # This prevents the ball from moving through paddles
        if self.ball.rect.colliderect(self.p1.rect):
            self.ball.bounce_paddle(self.p1)
        elif self.ball.rect.colliderect(self.p2.rect):
            self.ball.bounce_paddle(self.p2)
            
        # Update all objects (ball movement, paddle movement, etc.)
        super().update()
        
        # Check for scoring after movement
        if self.ball.scored_left:
            self.p2_score += 1
            # Check for winner
            if self.p2_score >= self.winning_score:
                return ("SCORE_SCREEN", "P2", self.p1_score, self.p2_score)
            self.ball.reset()
        elif self.ball.scored_right:
            self.p1_score += 1
            # Check for winner
            if self.p1_score >= self.winning_score:
                return ("SCORE_SCREEN", "P1", self.p1_score, self.p2_score)
            self.ball.reset()
        
        return None
