"""BrickBreakerLevel.py

Created on 2025-10-19

Brick Breaker game level scene.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .Raquette import Raquette
from .Ball import Ball


class BrickBreakerLevel(Scene):
    def __init__(self, players=1):
        super().__init__()
        self.paused = False
        self.num_players = players
        
        # Get screen dimensions
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Create paddle(s) at bottom
        self.p1 = Raquette("BRICK_P1")
        
        if players == 2:
            self.p2 = Raquette("BRICK_P2")
            self.add_object(self.p2)
        
        # Create balls for brick breaker (support multiple balls)
        self.balls = []
        initial_ball = Ball(game_mode="BRICK")
        initial_ball.reset()
        self.balls.append(initial_ball)
        
        # Initialize lives and score
        self.p1_lives = 3
        self.p2_lives = 3 if players == 2 else 0
        self.score = 0
        
        # TODO: Create bricks
        self.bricks = []
        
        # Add objects to scene
        self.add_object(self.p1)
        for ball in self.balls:
            self.add_object(ball)

    def check_balls_count(self):
        if len(self.balls) == 0:
            self.p1_lives -= 1
            if self.p1_lives <= 0:
                # Game Over - return tuple with final score
                return ("GAME_OVER", self.score)
            
            # Spawn new ball
            new_ball = Ball(game_mode="BRICK")
            new_ball.reset()
            self.balls.append(new_ball)
            self.add_object(new_ball)
    
    def update(self):
        """Update game state."""
        if self.paused:
            # Draw pause text
            font = pygame.font.Font(None, 74)
            screen = pygame.display.get_surface()
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            screen.blit(pause_text, pause_rect)
            return None
        
        # Check paddle collision for all balls
        for ball in self.balls:
            if ball.rect.colliderect(self.p1.rect):
                ball.bounce_paddle(self.p1)
            
            if self.num_players == 2 and ball.rect.colliderect(self.p2.rect):
                ball.bounce_paddle(self.p2)
        
        # Update all objects
        super().update()
        
        # Check if any balls fell off bottom (lose life)
        for ball in self.balls:
            # if update is not None:
            if ball.scored_bottom:
                self.balls.remove(ball)
                self.remove_object(ball)
                if self.check_balls_count() is not None:
                    return self.check_balls_count()

            for brick in self.bricks:
                if ball.rect.colliderect(brick.rect):
                    ball.bounce_brick(brick)
                    brick.destroy()
                    self.score += 10
        
        return None
