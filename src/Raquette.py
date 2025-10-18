"""Raquette.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .GameObject import GameObject


class Raquette(GameObject):
    # AI Difficulty levels with (speed, reaction_zone, error_margin)
    DIFFICULTY_EASY = {"speed": 200, "reaction_zone": 0.5, "error_margin": 50}
    DIFFICULTY_MEDIUM = {"speed": 350, "reaction_zone": 0.7, "error_margin": 20}
    DIFFICULTY_HARD = {"speed": 500, "reaction_zone": 0.9, "error_margin": 5}
    
    def __init__(self, type = "IA", difficulty="MEDIUM"):
        super().__init__()

        self.input_type = type
        self.is_ai = False
        self.ball_ref = None  # Reference to the ball for AI tracking
        self.ai_difficulty = difficulty

        match type:
            case "P1":
                self.keys = [pygame.K_UP, pygame.K_DOWN]

            case "P2":
                self.keys = [pygame.K_w, pygame.K_s]

            case "IA":
                self.keys = []
                self.is_ai = True
                # Set AI parameters based on difficulty
                if difficulty == "EASY":
                    self.ai_params = self.DIFFICULTY_EASY
                elif difficulty == "HARD":
                    self.ai_params = self.DIFFICULTY_HARD
                else:  # MEDIUM (default)
                    self.ai_params = self.DIFFICULTY_MEDIUM

        try:
            self.original = pygame.image.load(r"assets/images/Raquette.png").convert_alpha()
        except Exception as e: 

            # If image can't be loaded, create a placeholder surface
            print(f"Warning: could not load button image: {e}")
            self.original = pygame.Surface((200, 50), pygame.SRCALPHA)
            self.original.fill((100, 100, 100, 255))
        
        # Desired scale factor and rotation
        self.scale = 0.1  # scale down to 50%
        self.rotation = 90  # rotate 90 degrees clockwise

        # Create transformed image and rect
        try:
            w = max(1, int(self.original.get_width() * self.scale))
            h = max(1, int(self.original.get_height() * self.scale))
            scaled = pygame.transform.smoothscale(self.original, (w, h))
            self.background = pygame.transform.rotate(scaled, self.rotation)
        except Exception:
            # Fallback: use original if transforms fail
            self.background = self.original

        self.rect = self.background.get_rect()
        # Try to place the raquette depending on input type (P1 -> right side)
        self._pending_place = False
        try:
            screen = pygame.display.get_surface()
            if screen:
                sw, sh = screen.get_size()
                margin = 20
                if self.input_type == "P1":
                    x = sw - self.rect.width - margin
                else:
                    x = margin
                y = (sh - self.rect.height) // 2
                self.setPosition((x, y))
                self.rect.topleft = (int(x), int(y))
            else:
                # No surface yet; mark pending and will place on first update
                self._pending_place = True
        except Exception:
            self._pending_place = True

        # Movement speed in pixels per second (will be scaled by delta time)
        if self.is_ai:
            self.speed = self.ai_params["speed"]
        else:
            self.speed = 500
        # Time tracking for delta-time
        self._last_time = pygame.time.get_ticks()
        # Track paddle velocity for ball bounce calculations
        self.velocity_y = 0  # Current vertical velocity

    def set_ball(self, ball):
        """Set the ball reference for AI tracking."""
        self.ball_ref = ball

    def ai_update_position(self, dt):
        """AI logic to track and follow the ball.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.ball_ref:
            return
        
        # Get AI parameters
        speed = self.ai_params["speed"]
        reaction_zone = self.ai_params["reaction_zone"]
        error_margin = self.ai_params["error_margin"]
        
        # Only react if ball is in our reaction zone
        screen = pygame.display.get_surface()
        if not screen:
            return
            
        sw, sh = screen.get_size()
        ball_x = self.ball_ref.rect.centerx
        
        # Determine which side we're on and if ball is coming towards us
        is_right_side = self.rect.centerx > sw / 2
        ball_moving_towards_us = (is_right_side and self.ball_ref.velocity[0] > 0) or \
                                 (not is_right_side and self.ball_ref.velocity[0] < 0)
        
        # Calculate reaction threshold based on difficulty
        reaction_threshold = sw * reaction_zone
        should_react = False
        
        if is_right_side:
            # Right side AI reacts when ball crosses threshold from left
            should_react = ball_x > (sw - reaction_threshold) and ball_moving_towards_us
        else:
            # Left side AI reacts when ball crosses threshold from left
            should_react = ball_x < reaction_threshold and ball_moving_towards_us
        
        if not should_react:
            # Return to center when not actively tracking
            target_y = sh / 2
        else:
            # Track the ball with some error margin
            target_y = self.ball_ref.rect.centery
            # Add some imperfection based on difficulty
            import random
            if error_margin > 0:
                target_y += random.randint(-error_margin, error_margin)
        
        # Calculate current position
        x, y = self.position
        old_y = y
        paddle_center_y = y + self.rect.height / 2
        
        # Move towards target
        diff = target_y - paddle_center_y
        
        # Dead zone to prevent jittering
        if abs(diff) > 5:
            if diff < 0:
                y -= speed * dt
            else:
                y += speed * dt
        
        # Clamp to screen bounds
        y = max(0, min(y, sh - self.rect.height))
        
        # Calculate velocity (pixels per second)
        self.velocity_y = (y - old_y) / dt if dt > 0 else 0
        
        # Update position
        self.setPosition((x, y))
        self.rect.topleft = (int(x), int(y))

    def updatePosition(self, dt):
        """Handle keyboard input to move the raquette up and down.

        Uses arrow keys or W/S. Clamps the raquette to the current display surface.
        
        Args:
            dt: Delta time in seconds
        """

        try:
            keys = pygame.key.get_pressed()
        except Exception:
            keys = None

        # If placement was pending (no surface at init), place now
        if getattr(self, '_pending_place', False):
            try:
                screen = pygame.display.get_surface()
                if screen:
                    sw, sh = screen.get_size()
                    margin = 20
                    if self.input_type == "P1":
                        x = sw - self.rect.width - margin
                    else:
                        x = margin
                    y = (sh - self.rect.height) // 2
                    self.setPosition((x, y))
                    self.rect.topleft = (int(x), int(y))
                    self._pending_place = False
            except Exception:
                pass

        x, y = self.position
        old_y = y
        # Default to current rect top-left if position wasn't set
        try:
            x = int(x)
            y = int(y)
        except Exception:
            x, y = self.rect.topleft

        if keys:
            if keys[self.keys[0]]:
                y -= int(self.speed * dt)
            if keys[self.keys[1]]:
                y += int(self.speed * dt)

        # Clamp to screen bounds if a display surface exists
        try:
            screen = pygame.display.get_surface()
            if screen:
                sw, sh = screen.get_size()
                # Ensure the raquette stays within vertical bounds
                y = max(0, min(y, sh - self.rect.height))
        except Exception:
            pass

        # Calculate velocity (pixels per second)
        self.velocity_y = (y - old_y) / dt if dt > 0 else 0

        # Apply updated position and keep rect in sync
        self.setPosition((x, y))
        try:
            self.rect.topleft = (int(x), int(y))
        except Exception:
            pass

        return

    def update(self):
        # Compute delta time (in seconds)
        now = pygame.time.get_ticks()
        dt = (now - getattr(self, '_last_time', now)) / 1000.0
        # Clamp unreasonable dt values
        if dt > 0.5:
            dt = 0.5
        self._last_time = now

        if self.is_ai:
            self.ai_update_position(dt)
        else:
            self.updatePosition(dt)
        return None
    
    def render(self, screen):
        # Draw the transformed raquette at its position (top-left)
        try:
            screen.blit(self.background, self.position)
        except Exception:
            # If position is not set or blit fails, fall back to (0,0)
            screen.blit(self.background, (0, 0))
        return super().render(screen)
