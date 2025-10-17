"""PongLevel.py

Created on 2025-10-17



"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .Raquette import Raquette

class PongLevel(Scene):
    def __init__(self):
        super().__init__()
        test = Raquette()
        self.add_object(test)

    def update(self):
        return super().update()
    
    def update(self):
        return super().update()