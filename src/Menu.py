"""Menu.py

Created on 2025-10-16

Default Menu class. Used for Heritage

"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from .Scene import Scene
from .MenuButton import MenuButton


class Menu(Scene):
    def __init__(self):
        super().__init__()
        # Keyboard navigation
        self.selected_index = 0
        self.last_key_time = pygame.time.get_ticks()
        self.key_delay = 150  # ms between nav events
        self.using_keyboard = False  # Track if keyboard was last input
    
    def cleanup(self):
        """Clear selection state when menu is exited"""
        buttons = self.get_menu_buttons()
        for button in buttons:
            button.set_selected(False)

    def get_menu_buttons(self):
        # Return the list of MenuButton instances in renderable_objects
        return [obj for obj in self.renderable_objects if isinstance(obj, MenuButton)]

    def update(self):
        # Handle keyboard navigation and selection
        now = pygame.time.get_ticks()
        buttons = self.get_menu_buttons()
        
        if not buttons:
            return super().update()

        # Ensure valid selection index
        self.selected_index = max(0, min(self.selected_index, len(buttons) - 1))

        # Check if mouse moved
        rel = pygame.mouse.get_rel()
        if abs(rel[0]) > 0 or abs(rel[1]) > 0:
            # Mouse movement detected, switch to mouse mode
            if self.using_keyboard:
                self.using_keyboard = False
                buttons[self.selected_index].set_selected(False)

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if now - self.last_key_time > self.key_delay:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                # Switch to keyboard mode and move up
                if not self.using_keyboard:
                    self.using_keyboard = True
                buttons[self.selected_index].set_selected(False)
                self.selected_index = (self.selected_index - 1) % len(buttons)
                buttons[self.selected_index].set_selected(True)
                self.last_key_time = now
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                # Switch to keyboard mode and move down
                if not self.using_keyboard:
                    self.using_keyboard = True
                buttons[self.selected_index].set_selected(False)
                self.selected_index = (self.selected_index + 1) % len(buttons)
                buttons[self.selected_index].set_selected(True)
                self.last_key_time = now
            elif (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and self.using_keyboard:
                # Activate selected button if using keyboard
                return buttons[self.selected_index].return_state

        # Set initial selection if using keyboard
        if self.using_keyboard and not any(btn.is_selected for btn in buttons):
            buttons[self.selected_index].set_selected(True)

        # Handle mouse input through Scene.update
        return super().update()
