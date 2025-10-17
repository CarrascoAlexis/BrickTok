"""Raquette.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .GameObject import GameObject


class Raquette(GameObject):
    def __init__(self):
        super().__init__()

        try:
            self.backgorund = pygame.image.load(f"assets/images/Raquette.png")
        except Exception as e:
            # If image can't be loaded, create a placeholder surface
            print(f"Warning: could not load button image: {e}")
            self.background = pygame.Surface((200, 50), pygame.SRCALPHA)
            self.background.fill((100, 100, 100, 255))

        self.rect = self.background.get_rect()

    def update(self):
        
        return super().update()
    
    def render(self, screen):
        screen.blit(self.background, self.position)
        return super().render(screen)