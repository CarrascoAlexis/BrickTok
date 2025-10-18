"""game.py

Created on 2025-10-16

Main Game class managing overall state and scenes.

"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame

from .MainMenu import MainMenu
from .SettingsMenu import SettingsMenu
from .PongMenu import PongMenu
from .BrickMenu import BrickMenu
from .Scene import Scene
from .Menu import Menu
from .PongLevel import PongLevel
from .ScoreScreen import ScoreScreen

class Game:
    def __init__(self):
        """Initialize the main game class."""
        self.screen = None
        self.is_running = False
        self.fps_limit = 240
        self.state = 0
        self.scene = MainMenu()
        # Store game settings
        self.pong_players = 2
        self.pong_difficulty = "HARD"
        self.show_fps = False
        self.clock = None
        pass

    def changeState(self, new_state):
        """Change the current game state."""
        self.state = new_state
        return

    def setScreen(self, screen):
        """Set the main display screen for the game."""
        self.screen = screen
        pass

    def setScene(self, scene):
        """Set the current scene."""
        self.scene = scene

    def start(self):
        """Start the game loop."""
        self.is_running = True
        pass

    def stop(self):
        """Stop the game loop."""
        self.is_running = False

    def update(self):
        """Update the game state."""

        # Get the state and clean up the current scene if needed
        result = self.scene.update()
        if isinstance(self.scene, Menu):
            self.scene.cleanup()
        
        # Handle tuple results (for passing data between scenes)
        if isinstance(result, tuple):
            # Case for SCORE_SCREEN
            if result[0] == "SCORE_SCREEN":
                # result = ("SCORE_SCREEN", winner, p1_score, p2_score)
                winner = result[1]
                p1_score = result[2]
                p2_score = result[3]
                self.scene = ScoreScreen(winner, p1_score, p2_score)
                return None
            
        # Handle scene transitions
        match result:
            case "EXIT":
                self.stop()
            case "SETTINGS":
                self.scene = SettingsMenu()
            case "PLAY_PONG":
                self.scene = PongMenu()
            case "PLAY_BRICK":
                self.scene = BrickMenu()
            case "START_PONG":
                # Get settings from PongMenu if available
                if isinstance(self.scene, PongMenu):
                    player_count = self.scene.player_counts[self.scene.player_index]
                    difficulty = self.scene.difficulties[self.scene.diff_index].upper()
                    self.pong_players = player_count
                    self.pong_difficulty = difficulty
                self.scene = PongLevel(players=self.pong_players, difficulty=self.pong_difficulty)
            case "MAIN_MENU":
                self.scene = MainMenu()

        # If the current scene is the SettingsMenu, apply FPS settings to the game
        if isinstance(self.scene, SettingsMenu):
            self.fps_limit = int(self.scene.fps_options[self.scene.fps_index])

        return None
    
    def toggle_fps_display(self):
        self.show_fps = not self.show_fps
        return
    
    def handle_fps_display(self):
        fps = int(self.clock.get_fps())
        try:
            font = pygame.font.Font('assets/fonts/Vanilla Pancake.ttf', 18)
        except Exception:
            font = pygame.font.Font(None, 18)
        text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        bg = pygame.Surface((text.get_width() + 8, text.get_height() + 6))
        bg.set_alpha(180)
        bg.fill((0, 0, 0))
        self.screen.blit(bg, (10, 10))
        self.screen.blit(text, (14, 12))
        return

    def render(self):
        """Render the current scene."""
        # Clear screen for new render
        self.screen.fill("BLACK")

        # Check if scene is a Scene instance
        if isinstance(self.scene, Scene):
            self.scene.render(self.screen)
        
        if self.show_fps and self.clock:
            self.handle_fps_display()
