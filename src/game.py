"""game.py

Created on 2025-10-16


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

class Game:
    def __init__(self):
        self.screen = None
        self.is_running = False
        self.fps_limit = 60
        self.state = 0
        self.scene = MainMenu()
        pass

    def changeState(self, new_state):
        self.state = new_state
        return

    def setScreen(self, screen):
        self.screen = screen
        pass

    def setScene(self, scene):
        self.scene = scene

    def start(self):
        self.is_running = True
        pass

    def stop(self):
        self.is_running = False

    def update(self):
        # Get result from the active scene

        # Handle common scene results

        # Get the state and clean up the current scene if needed
        result = self.scene.update()
        if isinstance(self.scene, Menu):
            self.scene.cleanup()
            
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
                print("START PONG GAME")
                self.scene = PongLevel()
            case "MAIN_MENU":
                self.scene = MainMenu()

        # If the current scene exposes FPS settings, apply them to the game
        try:
            if hasattr(self.scene, 'fps_options') and hasattr(self.scene, 'fps_index'):
                self.fps_limit = int(self.scene.fps_options[self.scene.fps_index])
        except Exception:
            # Ignore any problems reading/applying fps from scene
            pass

        return None

    def render(self):
        # Clear screen for new render
        self.screen.fill("BLACK")
        if isinstance(self.scene, Scene):
            self.scene.render(self.screen)
        # Optional FPS overlay
        if getattr(self, 'show_fps', False) and hasattr(self, 'clock'):
            try:
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
            except Exception:
                pass
        pass
