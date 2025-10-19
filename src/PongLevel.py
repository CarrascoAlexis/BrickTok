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
from .MenuButton import MenuButton


class PongLevel(Scene):
    def __init__(self, players=2, difficulty="MEDIUM"):
        super().__init__()
        self.paused = False
        self.num_players = players

        # Pause cooldown to prevent rapid toggling
        self.last_pause_time = 0
        self.pause_cooldown = 300  # milliseconds

        # Create pause menu button
        self.menu_button = MenuButton("MAIN_MENU", "Menu principal")
        # Position button in center
        screen = pygame.display.get_surface()
        sw, sh = screen.get_size()
        btn_x = (sw - self.menu_button.rect.width) // 2
        btn_y = (sh + 100) // 2  # Below pause text
        self.menu_button.setPosition((btn_x, btn_y))
        self.menu_button.rect.topleft = (btn_x, btn_y)

        # Create paddles and position them
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        # Left paddle - always player 1
        self.p1 = Raquette("PONG_P1")

        # Right paddle - player 2 or AI depending on player count
        if players == 2:
            self.p2 = Raquette("PONG_P2")
        else:
            self.p2 = Raquette("PONG_IA", difficulty.upper())

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
            lambda: self.p2_score,
            isIA=(players == 1)
        )

        # Add all objects to scene (order matters for rendering)
        self.add_object(self.p1)
        self.add_object(self.p2)
        self.add_object(self.ball)
        self.add_object(self.score_display)

    def update(self):
        # Handle pause state with cooldown
        now = pygame.time.get_ticks()
        if pygame.key.get_pressed()[
                pygame.K_ESCAPE] and now - self.last_pause_time >= self.pause_cooldown:
            self.paused = not self.paused
            self.last_pause_time = now

        if self.paused:
            # Update menu button
            result = self.menu_button.update()
            if result == "MAIN_MENU":
                return "MAIN_MENU"
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
                return (
                    "SCORE_SCREEN",
                    "PONG_P2",
                    self.p1_score,
                    self.p2_score)
            self.ball.reset()
        elif self.ball.scored_right:
            self.p1_score += 1
            # Check for winner
            if self.p1_score >= self.winning_score:
                return (
                    "SCORE_SCREEN",
                    "PONG_P1",
                    self.p1_score,
                    self.p2_score)
            self.ball.reset()

        return None

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
            pause_rect = pause_text.get_rect(
                center=(
                    screen.get_width() // 2,
                    screen.get_height() // 2 - 50))
            screen.blit(pause_text, pause_rect)

            # Render menu button
            self.menu_button.render(screen)
