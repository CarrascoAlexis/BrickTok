"""GameObject.py

Created on 2025-10-16



"""
__author__ = "carras_a"
__version__ = "1.0"

import pygame


class GameObject():
    def __init__(self):
        self.is_dead = False
        self.position = (100, 100)

    def kill(self):
        self.is_dead = True

    def update(self):
        pass

    def setName(self, name):
        self.name = name

    def setPosition(self, position):
        self.position = position

    def handle_event(self, event):
        pass

    def render(self, screen):
        pass
