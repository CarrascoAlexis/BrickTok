"""Ball.py

Created on 2025-10-17

Ball class for both Pong and Brick Breaker games. Handles movement and collision.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
import random
import math
from .GameObject import GameObject
from .SoundManager import SoundManager


class Ball(GameObject):
    def __init__(self, game_mode="PONG"):
        super().__init__()
        
        # Game mode: "PONG" or "BRICK"
        self.game_mode = game_mode
        
        # Sound manager
        self.sound_manager = SoundManager()
        
        # Scoring flags
        self.scored_left = False
        self.scored_right = False
        self.scored_bottom = False  # For brick breaker
        
        # Load and scale ball sprite
        self.load_sprite()
        
        # Movement
        self.rect = self.background.get_rect()
        self.speed = 400  # pixels per second
        self.velocity = [0, 0]  # [vx, vy]
        self.waiting = True  # Wait for spacebar to start
        
        # Collision cooldown
        self.last_bounce_time = 0
        self.bounce_cooldown = 100  # milliseconds
        
        # Delta time tracking
        self.last_time = pygame.time.get_ticks()
        
        # Initial position
        self.reset()
    
    def load_sprite(self):
        """Load and scale the ball sprite."""
        try:
            original = pygame.image.load(r"assets/images/Ball.png").convert_alpha()
        except Exception:
            # Create white circle fallback
            size = 20
            original = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(original, (255, 255, 255), (size//2, size//2), size//2)
        
        # Scale to 50%
        w = max(1, int(original.get_width() * 0.5))
        h = max(1, int(original.get_height() * 0.5))
        self.background = pygame.transform.smoothscale(original, (w, h))

    def reset(self):
        """Reset ball to center with random direction."""
        self.scored_left = False
        self.scored_right = False
        self.scored_bottom = False
        self.waiting = True
        
        # Center on screen
        screen = pygame.display.get_surface()
        if screen:
            sw, sh = screen.get_size()
            x = (sw - self.rect.width) // 2
            
            # Different starting positions based on game mode
            if self.game_mode == "BRICK":
                y = sh - 150  # Start lower for brick breaker
            else:
                y = (sh - self.rect.height) // 2  # Center for pong
        else:
            x, y = 400, 300  # Fallback
        
        self.setPosition((x, y))
        self.rect.topleft = (x, y)
        
        # Set initial velocity based on game mode
        if self.game_mode == "BRICK":
            # Brick breaker: launch upward with random angle
            angle = random.uniform(-60, -120)  # Upward angles
        else:
            # Pong: random angle left or right
            angle = random.uniform(-45, 45)
            if random.random() < 0.5:
                angle += 180
        
        # Set velocity
        rad = math.radians(angle)
        self.velocity = [
            math.cos(rad) * self.speed,
            math.sin(rad) * self.speed
        ]

    def handle_event(self):
        """Handle spacebar to start ball movement."""
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.waiting = False
    
    def bounce_paddle(self, raquette):
        """Bounce off paddle - behavior depends on game mode."""
        # Cooldown check
        now = pygame.time.get_ticks()
        if now - self.last_bounce_time < self.bounce_cooldown:
            return
        self.last_bounce_time = now
        
        if self.game_mode == "PONG":
            # Pong: reverse horizontal direction
            self.velocity[0] = -self.velocity[0]
            
            # Add paddle's vertical velocity (50% influence)
            if hasattr(raquette, 'velocity_y'):
                self.velocity[1] += raquette.velocity_y * 0.5
            
            # Position ball outside paddle
            if self.velocity[0] > 0:
                self.rect.left = raquette.rect.right
            else:
                self.rect.right = raquette.rect.left
        
        elif self.game_mode == "BRICK":
            # Brick breaker: reverse vertical direction (bounce up)
            self.velocity[1] = -abs(self.velocity[1])  # Always bounce upward
            
            # Add paddle's horizontal velocity influence for angle control
            if hasattr(raquette, 'velocity_x'):
                # In brick breaker, paddle moves horizontally
                self.velocity[0] += raquette.velocity_x * 0.5
            
            # Position ball on top of paddle
            self.rect.bottom = raquette.rect.top
        
        self.setPosition(self.rect.topleft)
        
        # Sound effect
        self.sound_manager.play("paddle_hit", 0.5)

    def bounce_brick(self, brick):
        """Bounce off a brick - direction depends on which side was hit.
        
        Args:
            brick: The brick object that was hit (must have a rect attribute)
        """
        # Cooldown check to prevent multiple bounces
        now = pygame.time.get_ticks()
        if now - self.last_bounce_time < self.bounce_cooldown:
            return
        self.last_bounce_time = now
        
        # Calculate overlap on each side to determine which side was hit
        ball_rect = self.rect
        brick_rect = brick.rect
        
        # Calculate how much the ball overlaps the brick on each side
        overlap_left = ball_rect.right - brick_rect.left
        overlap_right = brick_rect.right - ball_rect.left
        overlap_top = ball_rect.bottom - brick_rect.top
        overlap_bottom = brick_rect.bottom - ball_rect.top
        
        # Find the smallest overlap to determine collision side
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
        
        if min_overlap == overlap_left or min_overlap == overlap_right:
            # Hit left or right side - reverse horizontal velocity
            self.velocity[0] = -self.velocity[0]
            
            # Position ball outside brick
            if min_overlap == overlap_left:
                self.rect.right = brick_rect.left
            else:
                self.rect.left = brick_rect.right
        else:
            # Hit top or bottom side - reverse vertical velocity
            self.velocity[1] = -self.velocity[1]
            
            # Position ball outside brick
            if min_overlap == overlap_top:
                self.rect.bottom = brick_rect.top
            else:
                self.rect.top = brick_rect.bottom
        
        self.setPosition(self.rect.topleft)
        
        # Sound effect
        self.sound_manager.play("wall_hit", 0.4)

    def update(self):
        """Update ball position and handle collisions."""
        # Check for spacebar press
        
        if self.waiting:
            self.handle_event()
            return None
        
        # Calculate delta time
        now = pygame.time.get_ticks()
        dt = (now - self.last_time) / 1000.0
        dt = min(dt, 0.5)  # Cap at 0.5s to avoid huge jumps
        self.last_time = now
        
        # Move ball
        x, y = self.position
        x += self.velocity[0] * dt
        y += self.velocity[1] * dt
        
        # Get screen dimensions
        screen = pygame.display.get_surface()
        if not screen:
            return None
        sw, sh = screen.get_size()
        
        # Vertical wall bounces (top/bottom)
        if y < 0:
            y = 0
            self.velocity[1] = abs(self.velocity[1])
            self.sound_manager.play("wall_hit", 0.3)
        elif y + self.rect.height > sh:
            # Different behavior based on game mode
            if self.game_mode == "BRICK":
                # Brick breaker: ball fell off bottom (lose life)
                self.scored_bottom = True
                return "SCORE"
            else:
                # Pong: bounce off bottom
                y = sh - self.rect.height
                self.velocity[1] = -abs(self.velocity[1])
                self.sound_manager.play("wall_hit", 0.3)
        
        # Horizontal bounds
        if self.game_mode == "PONG":
            # Pong: scoring on left/right
            if x < 0:
                self.scored_left = True
                return "SCORE"
            if x + self.rect.width > sw:
                self.scored_right = True
                return "SCORE"
        else:
            # Brick breaker: bounce off left/right walls
            if x < 0:
                x = 0
                self.velocity[0] = abs(self.velocity[0])
                self.sound_manager.play("wall_hit", 0.3)
            elif x + self.rect.width > sw:
                x = sw - self.rect.width
                self.velocity[0] = -abs(self.velocity[0])
                self.sound_manager.play("wall_hit", 0.3)
        
        # Update position
        self.setPosition((x, y))
        self.rect.topleft = (int(x), int(y))
        
        return None

    def render(self, screen):
        """Draw the ball."""
        screen.blit(self.background, self.position)
        
        # Show "PRESS SPACE" text when waiting
        if self.waiting:
            font = pygame.font.Font(None, 36)
            text = font.render("PRESS SPACE", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2 + 50)
            )
            screen.blit(text, text_rect)
        
        return super().render(screen)
