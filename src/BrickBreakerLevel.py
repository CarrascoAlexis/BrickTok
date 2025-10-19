"""BrickBreakerLevel.py

Created on 2025-10-19

Brick Breaker game level scene.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
import os
from .Scene import Scene
from .Raquette import Raquette
from .Ball import Ball
from .Brick import Brick


class BrickBreakerLevel(Scene):
    def __init__(self, players=1, level_number=1):
        super().__init__()
        self.paused = False
        self.num_players = players
        self.level_number = level_number
        
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
        
        # Load level and create bricks
        self.bricks = []
        self._load_level(level_number)
        
        # Add objects to scene
        self.add_object(self.p1)
        for ball in self.balls:
            self.add_object(ball)
        for brick in self.bricks:
            self.add_object(brick)
    
    def _load_level(self, level_number):
        """Load level layout from file.
        
        Args:
            level_number: Level number to load (1-based)
        """
        # Format level filename with leading zeros
        level_file = f"levels/level_{level_number:03d}.txt"
        
        if not os.path.exists(level_file):
            print(f"Warning: Level file {level_file} not found. Creating empty level.")
            return
        
        try:
            with open(level_file, 'r') as f:
                lines = f.readlines()
            
            # Get screen dimensions for brick positioning
            screen = pygame.display.get_surface()
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            
            # Parse level data
            brick_width = 80
            brick_height = 30
            margin_x = 10
            margin_y = 10  # Start from top of screen
            spacing_x = 5
            spacing_y = 5
            
            # Filter out comment lines and empty lines first
            brick_rows = []
            for line in lines:
                line = line.rstrip()  # Keep leading spaces but remove trailing
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    brick_rows.append(line)
            
            for row_idx, line in enumerate(brick_rows):
                for col_idx, char in enumerate(line):
                    if char == ' ' or char == '.':  # Empty space
                        continue
                    
                    # Determine brick type based on character
                    brick_type = self._get_brick_type(char)
                    
                    # Calculate position - starts from top
                    x = margin_x + col_idx * (brick_width + spacing_x)
                    y = margin_y + row_idx * (brick_height + spacing_y)
                    
                    # Create brick
                    brick = Brick(x, y, brick_width, brick_height, brick_type)
                    self.bricks.append(brick)
        
        except Exception as e:
            print(f"Error loading level {level_number}: {e}")
    
    def _get_brick_type(self, char):
        """Convert character to brick type.
        
        Args:
            char: Character from level file
            
        Returns:
            Brick type string
        """
        brick_map = {
            'R': 'red',
            'O': 'orange',
            'Y': 'yellow',
            'G': 'green',
            'B': 'blue',
            'P': 'purple',
            'X': 'gray',
        }
        return brick_map.get(char.upper(), 'red')

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
        
        # Check brick collisions and remove destroyed bricks
        bricks_to_remove = []
        for ball in self.balls:
            for brick in self.bricks:
                if not brick.is_destroyed() and ball.rect.colliderect(brick.rect):
                    ball.bounce_brick(brick)
                    if brick.take_damage():
                        # Brick destroyed
                        bricks_to_remove.append(brick)
                        self.score += brick.get_points()
        
        # Remove destroyed bricks
        for brick in bricks_to_remove:
            self.bricks.remove(brick)
            self.remove_object(brick)
        
        # Check if all bricks are destroyed (level complete)
        if len(self.bricks) == 0:
            return ("LEVEL_COMPLETE", self.level_number, self.score)
        
        # Check if any balls fell off bottom (lose life)
        balls_to_remove = []
        for ball in self.balls:
            if ball.scored_bottom:
                balls_to_remove.append(ball)
        
        # Remove balls that fell off
        for ball in balls_to_remove:
            self.balls.remove(ball)
            self.remove_object(ball)
        
        # If no balls left, lose a life and spawn new ball
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
        
        return None
