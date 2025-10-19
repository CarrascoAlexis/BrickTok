"""Brick.py

Created on 2025-10-19

Brick class for Brick Breaker game.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .GameObject import GameObject


class Brick(GameObject):
    """A brick that can be destroyed by the ball.
    
    Different brick types have different colors, health, and point values.
    """
    
    # Brick type definitions: (color, health, points)
    BRICK_TYPES = {
        "red": ((220, 50, 50), 1, 10),
        "orange": ((255, 140, 0), 1, 10),
        "yellow": ((255, 215, 0), 1, 10),
        "green": ((50, 205, 50), 2, 20),
        "blue": ((70, 130, 255), 2, 20),
        "purple": ((148, 0, 211), 3, 30),
        "gray": ((128, 128, 128), 5, 50),
    }
    
    def __init__(self, x, y, width=80, height=30, brick_type="red"):
        """Initialize a brick.
        
        Args:
            x: X position
            y: Y position
            width: Brick width in pixels
            height: Brick height in pixels
            brick_type: Type of brick ("red", "orange", "yellow", "green", "blue", "purple", "gray")
        """
        super().__init__()
        
        self.brick_type = brick_type
        self.width = width
        self.height = height
        
        # Get brick properties
        if brick_type in self.BRICK_TYPES:
            self.color, self.max_health, self.points = self.BRICK_TYPES[brick_type]
        else:
            # Default to red if invalid type
            self.color, self.max_health, self.points = self.BRICK_TYPES["red"]
        
        self.health = self.max_health
        self.destroyed = False
        
        # Create brick surface
        self.create_surface()
        
        # Set position
        self.rect = self.background.get_rect()
        self.setPosition((x, y))
        self.rect.topleft = (int(x), int(y))
    
    def create_surface(self):
        """Create the brick's visual surface."""
        # Create main brick surface
        self.background = pygame.Surface((self.width, self.height))
        
        # Fill with brick color
        self.background.fill(self.color)
        
        # Add border for 3D effect
        border_color = tuple(min(c + 40, 255) for c in self.color)  # Lighter border
        shadow_color = tuple(max(c - 40, 0) for c in self.color)  # Darker shadow
        
        # Draw highlights (top and left)
        pygame.draw.line(self.background, border_color, (0, 0), (self.width - 1, 0), 2)  # Top
        pygame.draw.line(self.background, border_color, (0, 0), (0, self.height - 1), 2)  # Left
        
        # Draw shadows (bottom and right)
        pygame.draw.line(self.background, shadow_color, (0, self.height - 1), (self.width - 1, self.height - 1), 2)  # Bottom
        pygame.draw.line(self.background, shadow_color, (self.width - 1, 0), (self.width - 1, self.height - 1), 2)  # Right
        
        # Add health indicator if health > 1
        if self.health > 1:
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.health), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.background.blit(text, text_rect)
    
    def take_damage(self, damage=1):
        """Reduce brick health by damage amount.
        
        Args:
            damage: Amount of damage to deal (default: 1)
            
        Returns:
            True if brick was destroyed, False otherwise
        """
        self.health -= damage
        
        if self.health <= 0:
            self.destroyed = True
            return True
        else:
            # Update visual to show new health
            self.create_surface()
            return False
    
    def destroy(self):
        """Instantly destroy the brick."""
        self.health = 0
        self.destroyed = True
    
    def is_destroyed(self):
        """Check if brick is destroyed.
        
        Returns:
            True if destroyed, False otherwise
        """
        return self.destroyed
    
    def get_points(self):
        """Get the point value of this brick.
        
        Returns:
            Integer point value
        """
        return self.points
    
    def update(self):
        """Update brick state."""
        # Bricks don't need to update unless you want animations
        return None
    
    def render(self, screen):
        """Render the brick on screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.destroyed:
            screen.blit(self.background, self.rect)
