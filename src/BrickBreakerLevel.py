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
from .MenuButton import MenuButton


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

        # Pause cooldown to prevent rapid toggling
        self.last_key_pressed = 0
        self.key_cooldown = 150  # milliseconds

        self.is_hanihilator = False

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
        self.menu_button = MenuButton("MAIN_MENU", "Menu principal")
        # Position button in center
        screen = pygame.display.get_surface()
        sw, sh = screen.get_size()
        btn_x = (sw - self.menu_button.rect.width) // 2
        btn_y = (sh + 100) // 2  # Below pause text
        self.menu_button.setPosition((btn_x, btn_y))
        self.menu_button.rect.topleft = (btn_x, btn_y)

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

        self.paused = False

    def _load_level(self, level_number):
        """Load level layout from file.

        Args:
            level_number: Level number to load (1-based)
        """
        # Format level filename with leading zeros
        level_file = f"levels/level_{level_number:03d}.txt"

        if not os.path.exists(level_file):
            print(
                f"Warning: Level file {level_file} not found. Creating empty level.")
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
            spacing_x = 5
            spacing_y = 5
            margin_y = 10  # Top margin

            # Filter out comment lines and empty lines first
            brick_rows = []
            max_row_length = 0
            for line in lines:
                line = line.rstrip()  # Keep leading spaces but remove trailing
                if line and not line.startswith(
                        '#'):  # Skip empty lines and comments
                    brick_rows.append(line)
                    max_row_length = max(max_row_length, len(line))

            # Calculate total width needed for the longest row
            total_width_needed = max_row_length * \
                (brick_width + spacing_x) - spacing_x

            # Check if bricks fit on screen, if not scale them down
            available_width = screen_width - 20  # 10px margin on each side
            if total_width_needed > available_width:
                # Scale down brick width to fit
                scale_factor = available_width / total_width_needed
                brick_width = int(brick_width * scale_factor)
                spacing_x = int(spacing_x * scale_factor)
                total_width_needed = max_row_length * \
                    (brick_width + spacing_x) - spacing_x

            # Calculate horizontal offset to center the brick grid
            margin_x = (screen_width - total_width_needed) // 2

            # Limit number of rows to prevent overflow
            max_rows = (screen_height - margin_y -
                        200) // (brick_height + spacing_y)
            if len(brick_rows) > max_rows:
                print(
                    f"Warning: Level has {
                        len(brick_rows)} rows, limiting to {max_rows} to fit screen")
                brick_rows = brick_rows[:max_rows]

            for row_idx, line in enumerate(brick_rows):
                for col_idx, char in enumerate(line):
                    if char == ' ' or char == '.':  # Empty space
                        continue

                    # Determine brick type based on character
                    brick_type = self.get_brick_type(char)

                    # Calculate position - centered horizontally
                    x = margin_x + col_idx * (brick_width + spacing_x)
                    y = margin_y + row_idx * (brick_height + spacing_y)

                    # Create brick
                    brick = Brick(x, y, brick_width, brick_height, brick_type)
                    self.bricks.append(brick)

        except Exception as e:
            print(f"Error loading level {level_number}: {e}")

    def get_brick_type(self, char):
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

    def update_keys(self):
        now = pygame.time.get_ticks()
        if now - self.last_key_pressed < self.key_cooldown:
            return
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.paused = not self.paused
            self.last_key_pressed = now
        if key[pygame.K_h]:
            self.is_hanihilator = not self.is_hanihilator
        if key[pygame.K_F10]:
            for brick in self.bricks:
                self.remove_object(brick)
            self.bricks.clear()
            # Trigger level complete
            return ("LEVEL_COMPLETE", self.level_number, self.score)

        self.last_key_pressed = now
        return None

    def update(self):
        """Update game state."""
        # Handle pause state with cooldown

        if self.paused:
            # Update menu button
            result = self.menu_button.update()
            if result == "MAIN_MENU":
                return "MAIN_MENU"
            return None
        # Format level filename with leading zeros
        if self.is_hanihilator:
            ball = Ball(game_mode="BRICK", has_to_wait=False)
            ball.setPosition((self.p1.rect.centerx, self.p1.rect.top - 20))
            self.balls.append(ball)
            self.add_object(ball)

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

        return self.update_keys()

    def render(self, screen):
        # Always render game objects first
        super().render(screen)

        # Then render pause overlay on top if paused
        if self.paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Pause text
            font = pygame.font.Font(None, 74)
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(
                screen.get_width() // 2, screen.get_height() // 2 - 50))
            screen.blit(pause_text, pause_rect)

            # Render menu button
            return self.menu_button.render(screen)
