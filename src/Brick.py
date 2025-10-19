"""Brick.py

Created on 2025-10-19

Brick class for Brick Breaker game.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .GameObject import GameObject


class Brick(GameObject):
    """A destructible brick for the Brick Breaker game.

    Bricks have different types with varying colors, health, and point
    values. They can take damage and be destroyed when hit by the ball.
    Visual appearance includes 3D borders and health indicators.

    Attributes:
        brick_type (str): Type identifier (red, orange, yellow, etc.).
        width (int): Brick width in pixels.
        height (int): Brick height in pixels.
        color (tuple): RGB color tuple.
        max_health (int): Maximum health points.
        health (int): Current health points.
        points (int): Points awarded when destroyed.
        destroyed (bool): True if brick has been destroyed.
        rect (pygame.Rect): Collision rectangle.

    Class Attributes:
        BRICK_TYPES (dict): Maps brick type to (color, health, points).
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
        """Initialize a brick at the specified position.

        Creates a brick with the specified dimensions and type. Loads
        properties from BRICK_TYPES dictionary. Defaults to red brick
        if invalid type is provided.

        Args:
            x (float): X coordinate in pixels.
            y (float): Y coordinate in pixels.
            width (int): Brick width in pixels (default: 80).
            height (int): Brick height in pixels (default: 30).
            brick_type (str): Brick type identifier (default: "red").
        """
        super().__init__()

        self.brick_type = brick_type
        self.width = width
        self.height = height

        # Get brick properties
        if brick_type in self.BRICK_TYPES:
            self.color, self.max_health, self.points = (
                self.BRICK_TYPES[brick_type])
        else:
            # Default to red if invalid type
            self.color, self.max_health, self.points = (
                self.BRICK_TYPES["red"])

        self.health = self.max_health
        self.destroyed = False

        # Create brick surface
        self.create_surface()

        # Set position
        self.rect = self.background.get_rect()
        self.setPosition((x, y))
        self.rect.topleft = (int(x), int(y))

    def create_surface(self):
        """Create and render the brick's visual appearance.

        Generates a colored rectangle with 3D border effects (highlights
        on top/left, shadows on bottom/right). If health is greater than 1,
        displays health value as white text in the center.
        """
        # Create main brick surface
        self.background = pygame.Surface((self.width, self.height))

        # Fill with brick color
        self.background.fill(self.color)

        # Add border for 3D effect
        border_color = tuple(min(c + 40, 255)
                             for c in self.color)  # Lighter border
        shadow_color = tuple(max(c - 40, 0)
                             for c in self.color)  # Darker shadow

        # Draw highlights (top and left)
        pygame.draw.line(self.background, border_color,
                         (0, 0), (self.width - 1, 0), 2)  # Top
        pygame.draw.line(self.background, border_color,
                         (0, 0), (0, self.height - 1), 2)  # Left

        # Draw shadows (bottom and right)
        pygame.draw.line(
            self.background,
            shadow_color,
            (0,
             self.height - 1),
            (self.width - 1,
             self.height - 1),
            2)  # Bottom
        pygame.draw.line(
            self.background,
            shadow_color,
            (self.width - 1,
             0),
            (self.width - 1,
             self.height - 1),
            2)  # Right

        # Add health indicator if health > 1
        if self.health > 1:
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.health), True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2))
            self.background.blit(text, text_rect)

    def take_damage(self, damage=1):
        """Apply damage to the brick and check if destroyed.

        Reduces health by the specified damage amount. If health reaches
        zero or below, marks brick as destroyed. Updates visual appearance
        to reflect new health value.

        Args:
            damage (int): Amount of damage to apply (default: 1).

        Returns:
            bool: True if brick was destroyed by this damage, False if still
                  alive.
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
        """Instantly destroy the brick regardless of health.

        Sets health to 0 and marks brick as destroyed. Used for power-ups
        or special effects that instantly destroy bricks.
        """
        self.health = 0
        self.destroyed = True

    def is_destroyed(self):
        """Check the destroyed state of the brick.

        Returns:
            bool: True if brick has been destroyed, False otherwise.
        """
        return self.destroyed

    def get_points(self):
        """Get the point value awarded for destroying this brick.

        Returns:
            int: Point value of the brick.
        """
        return self.points

    def update(self):
        """Update the brick's state.

        Currently bricks are static and don't require updates. This method
        exists for consistency with the GameObject interface and can be
        extended for animations or special effects.

        Returns:
            None: Always returns None.
        """
        # Bricks don't need to update unless you want animations
        return None

    def render(self, screen):
        """Render the brick to the screen if not destroyed.

        Draws the brick's surface at its current position. Destroyed bricks
        are not rendered.

        Args:
            screen (pygame.Surface): The surface to render to.
        """
        if not self.destroyed:
            screen.blit(self.background, self.rect)
