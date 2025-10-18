"""Ball.py

Created on 2025-10-17

Ball class for Pong game. Handles movement, collision with raquettes,
and bouncing off screen edges.
"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
import random
import math
from .GameObject import GameObject
from .SoundManager import SoundManager


class Ball(GameObject):
    def __init__(self):
        super().__init__()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        self.scored_left = False
        self.scored_right = False
        
        # Load ball sprite or create a fallback circle
        try:
            self.original = pygame.image.load(r"assets/images/Ball.png").convert_alpha()
        except Exception as e:
            print(f"Warning: could not load ball image: {e}")
            # Create a white circle as fallback
            size = 20
            self.original = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.original, (255, 255, 255), (size//2, size//2), size//2)

        # Scale the ball sprite
        try:
            self.scale = 0.5  # 10% of original size
            w = max(1, int(self.original.get_width() * self.scale))
            h = max(1, int(self.original.get_height() * self.scale))
            self.background = pygame.transform.smoothscale(self.original, (w, h))
        except Exception:
            self.background = self.original

        # Movement and collision
        self.rect = self.background.get_rect()
        self.base_speed = 400  # base pixels per second
        self.speed = self.base_speed
        self._last_time = pygame.time.get_ticks()
        self._start_time = None  # Time when ball starts moving
        self.speed_increase_rate = 0.05  # 5% speed increase per second
        self.max_speed_multiplier = 3.0  # Maximum 3x speed
        self.waiting = True  # Ball waits for spacebar before moving
        self._last_bounce_time = 0  # Prevent multiple bounces on same paddle
        self._bounce_cooldown = 100  # milliseconds between bounces
        
        # Initial position and velocity
        self.reset()

    def reset(self):
        """Reset ball to center with random direction."""
        self.scored_left = False
        self.scored_right = False
        self.waiting = True  # Wait for spacebar press
        self._start_time = None  # Reset start time
        self.speed = self.base_speed  # Reset to base speed
        try:
            # Center the ball on screen
            screen = pygame.display.get_surface()
            if screen:
                sw, sh = screen.get_size()
                x = (sw - self.rect.width) // 2
                y = (sh - self.rect.height) // 2
                self.setPosition((x, y))
                self.rect.topleft = (x, y)
        except Exception:
            # Fallback to a reasonable position
            self.setPosition((400, 300))
            self.rect.topleft = (400, 300)

        # Random angle between -45 and 45 degrees (avoid too vertical angles)
        angle = random.uniform(-45, 45)
        # Random initial direction (left or right)
        if random.random() < 0.5:
            angle += 180

        # Convert angle to velocity components
        rad = math.radians(angle)
        self.velocity = [
            math.cos(rad) * self.speed,
            math.sin(rad) * self.speed
        ]

    def handle_event(self, event):
        """Handle keyboard events for ball launch."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.waiting:
                self.waiting = False  # Start ball movement
                self._last_time = pygame.time.get_ticks()  # Reset time to avoid big jump
                self._start_time = pygame.time.get_ticks()  # Track when ball starts moving

    def check_raquette_collision(self, raquettes):
        """Check and handle collision with raquettes."""
        for raquette in raquettes:
            if self.rect.colliderect(raquette.rect):
                # Find collision side (left or right of the ball)
                if self.rect.centerx < raquette.rect.centerx:
                    # Hit from right side - bounce left
                    self.rect.right = raquette.rect.left
                    self.velocity[0] = -abs(self.velocity[0])  # Ensure moving left
                else:
                    # Hit from left side - bounce right
                    self.rect.left = raquette.rect.right
                    self.velocity[0] = abs(self.velocity[0])  # Ensure moving right

                # Add some angle based on where the ball hits the paddle
                # Higher/lower hits result in steeper angles
                relative_intersect_y = (raquette.rect.centery - self.rect.centery)
                normalized_intersect = relative_intersect_y / (raquette.rect.height / 2)
                bounce_angle = normalized_intersect * 60  # max 60 degree bounce
                
                # Update velocity with new angle while preserving speed
                speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
                rad = math.radians(bounce_angle)
                self.velocity[1] = -math.sin(rad) * speed

                # Slightly increase speed on each bounce
                self.velocity = [v * 1.05 for v in self.velocity]
                
                # Play paddle hit sound
                self.sound_manager.play("paddle_hit", 0.5)
                return True
        return False
    
    def bounce_paddle(self, raquette):
        """Bounce off paddle - reverse horizontal direction and add paddle velocity influence."""
        # Check bounce cooldown to prevent multiple bounces
        now = pygame.time.get_ticks()
        if now - self._last_bounce_time < self._bounce_cooldown:
            return  # Too soon to bounce again
        self._last_bounce_time = now
        
        # Reverse horizontal direction
        self.velocity[0] = -self.velocity[0]
        
        # Add paddle's vertical velocity to the ball's vertical velocity
        # Scale the paddle influence (0.5 = 50% of paddle's velocity is transferred)
        paddle_influence = 0.5
        if hasattr(raquette, 'velocity_y'):
            self.velocity[1] += raquette.velocity_y * paddle_influence

        # Nudge ball outside the paddle to prevent re-collision next frame
        if self.velocity[0] > 0:
            # Going right - place ball to the right of paddle
            self.rect.left = raquette.rect.right
        else:
            # Going left - place ball to the left of paddle
            self.rect.right = raquette.rect.left
        
        # Keep internal position in sync
        self.setPosition(self.rect.topleft)

        # Sound effect
        self.sound_manager.play("paddle_hit", 0.5)
        return

    def update(self, raquettes=None):
        """Update ball position, handle collisions with screen edges and raquettes."""
        # If waiting for spacebar, don't move
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.waiting = False
            if self._start_time is None:
                self._start_time = pygame.time.get_ticks()

        if self.waiting:
            return None
            
        # Get time since last update
        now = pygame.time.get_ticks()
        dt = (now - self._last_time) / 1000.0
        if dt > 0.5: dt = 0.5  # Avoid huge jumps
        self._last_time = now

        # Calculate speed multiplier based on time elapsed
        if self._start_time is not None:
            time_elapsed = (now - self._start_time) / 1000.0  # seconds
            speed_multiplier = 1.0 + (self.speed_increase_rate * time_elapsed)
            speed_multiplier = min(speed_multiplier, self.max_speed_multiplier)  # Cap at max
            self.speed = self.base_speed * speed_multiplier
            
            # Update velocity magnitude to match new speed
            current_speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
            if current_speed > 0:
                scale = self.speed / current_speed
                self.velocity[0] *= scale
                self.velocity[1] *= scale

        # Update position
        x, y = self.position
        x += self.velocity[0] * dt
        y += self.velocity[1] * dt

        # Screen boundary collisions
        try:
            screen = pygame.display.get_surface()
            if screen:
                sw, sh = screen.get_size()
                
                # Vertical bounds (top/bottom)
                if y < 0:
                    y = 0
                    self.velocity[1] = abs(self.velocity[1])  # Bounce down
                    self.sound_manager.play("wall_hit", 0.3)
                elif y + self.rect.height > sh:
                    y = sh - self.rect.height
                    self.velocity[1] = -abs(self.velocity[1])  # Bounce up
                    self.sound_manager.play("wall_hit", 0.3)

                # Horizontal bounds (left/right) - trigger reset
                if x < 0:
                    self.scored_left = True
                    return "SCORE"  # Let the scene handle scoring 
                if x + self.rect.width > sw:
                    self.scored_right = True
                    return "SCORE"  # Let the scene handle scoring
        except Exception:
            pass

        # Update position and rect
        self.setPosition((x, y))
        self.rect.topleft = (int(x), int(y))

        # NOTE: Paddle collision is now handled in PongLevel.update()
        # to use the angle-based bounce_paddle() method

        return None

    def render(self, screen):
        """Draw the ball at its current position."""
        try:
            screen.blit(self.background, self.position)
            
            # Show "PRESS SPACE" text when waiting
            if self.waiting:
                font = pygame.font.Font(None, 36)
                text = font.render("PRESS SPACE", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
                screen.blit(text, text_rect)
        except Exception:
            # Fallback to (0,0) if position invalid
            screen.blit(self.background, (0, 0))
        return super().render(screen)