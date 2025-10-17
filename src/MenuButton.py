"""MenuButton.py

Created on 2025-10-16

Menu Button class

"""
__author__ = "carras_a"
__version__ = "1.0"


from .GameObject import GameObject
import pygame
import random


class MenuButton(GameObject):
    def __init__(self, return_state=None, text=""):
        super().__init__()
        # State to return when the button is clicked
        self.return_state = return_state
        self.text = text

        # Click delay for sensitive actions (like EXIT)
        self.click_delay = 500 if return_state == "EXIT" else 150  # 500ms delay for exit
        self.last_click_time = pygame.time.get_ticks()

        # Load a random background image (safe fallback)
        try:
            self.background = pygame.image.load(f"assets/images/Button_0{random.randint(1, 3)}.png").convert_alpha()
        except Exception as e:
            # If image can't be loaded, create a placeholder surface
            print(f"Warning: could not load button image: {e}")
            self.background = pygame.Surface((200, 50), pygame.SRCALPHA)
            self.background.fill((100, 100, 100, 255))

        # Create rect and align to initial position
        self.rect = self.background.get_rect()

        # Load font from assets (Vanilla Pancake). Size based on button height.
        font_size = max(12, int(self.rect.height * 0.5))
        try:
            self.font = pygame.font.Font("assets/fonts/Vanilla Pancake.ttf", font_size)
        except Exception:
            # Fallback to default font if custom font can't be loaded
            self.font = pygame.font.Font(None, font_size)

        # Click handling
        self.was_pressed = False  # Debounce previous mouse state
        # Selection state for keyboard navigation
        self.is_selected = False
        # Hover state for mouse
        self.is_hovered = False
        # Scale animation
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.18

    def update(self):
        """Auto-update called from game loop. Returns self.return_state when clicked, otherwise None."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        current_time = pygame.time.get_ticks()

        clicked = False
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered:
            if mouse_pressed and not self.was_pressed:
                # Check if enough time has passed since last click
                if current_time - self.last_click_time >= self.click_delay:
                    clicked = True
                    self.last_click_time = current_time

        # Update target scale based on hover or selection
        if self.is_hovered or self.is_selected:
            self.target_scale = 1.06
        else:
            self.target_scale = 1.0

        # Smoothly interpolate current scale towards target
        self.scale += (self.target_scale - self.scale) * self.scale_speed

        # Update debounce state
        self.was_pressed = mouse_pressed

        if clicked:
            return self.return_state
        return None

    def render(self, screen):
        # Draw scaled button (scale around center)
        try:
            sw = max(1, int(self.rect.width * self.scale))
            sh = max(1, int(self.rect.height * self.scale))
            scaled = pygame.transform.smoothscale(self.background, (sw, sh))
            blit_x = self.rect.centerx - sw // 2
            blit_y = self.rect.centery - sh // 2
            screen.blit(scaled, (blit_x, blit_y))

            # Draw text centered on scaled rect
            if getattr(self, 'text', None):
                try:
                    # Choose text color based on state
                    if self.is_selected or self.is_hovered:
                        text_color = (0, 100, 200)  # Lighter blue for hover
                    else:
                        text_color = (0, 0, 0)  # Black for normal state
                    
                    text_surface = self.font.render(self.text, True, text_color)
                except Exception:
                    fallback_font = pygame.font.Font(None, max(12, int(self.rect.height * 0.5)))
                    text_surface = fallback_font.render(self.text, True, (255, 255, 255))

                text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
                # shadow (slightly darker version of text color)
                try:
                    shadow_color = tuple(max(0, c - 50) for c in text_color)
                    shadow_surf = self.font.render(self.text, True, shadow_color)
                    shadow_rect = text_rect.copy()
                    shadow_rect.x += 2
                    shadow_rect.y += 2
                    screen.blit(shadow_surf, shadow_rect)
                except Exception:
                    pass
                screen.blit(text_surface, text_rect)
        except Exception:
            # Fallback to original draw if scaling fails
            screen.blit(self.background, self.rect)
            if getattr(self, 'text', None):
                text_surface = self.font.render(self.text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)

        return super().render(screen)

    def checkPressed(self, position):
        return self.rect.collidepoint(*position)

    def setPosition(self, position):
        """Override to keep rect in sync with GameObject position."""
        super().setPosition(position)
        # position may be a tuple (x,y)
        try:
            self.rect.topleft = self.position
        except Exception:
            pass

    def set_selected(self, selected: bool):
        """Set keyboard selection state. Visual feedback drawn in render()."""
        self.is_selected = bool(selected)