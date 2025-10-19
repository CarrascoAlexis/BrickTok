"""BrickTok -main.py

Created on 2025-10-15

This project is the bonus project for 2nd week at ETNA POOL


"""
__author__ = "carras_a"
__version__ = "1.0"


import pygame
from src.game import Game


def main():
    """Initialize and run the main game loop.

    This function initializes pygame, sets up the display with fullscreen mode,
    creates the game instance, and runs the main game loop handling events,
    updates, and rendering.
    """
    pygame.init()
    # Try to get the desktop resolution reliably
    sizes = pygame.display.get_desktop_sizes()
    # get_desktop_sizes returns a list of (w,h) tuples; use first/primary
    width, height = sizes[0]

    # Track fullscreen state and windowed size
    fullscreen = True
    windowed_size = (800, 600)

    def set_display_mode(fullscreen_mode: bool):
        """Set the display mode to fullscreen or windowed.

        Args:
            fullscreen_mode (bool): True for fullscreen, False for windowed.
        """
        nonlocal fullscreen, screen
        fullscreen = bool(fullscreen_mode)
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if fullscreen:
            flags |= pygame.FULLSCREEN
            screen = pygame.display.set_mode((width, height), flags)
        else:
            screen = pygame.display.set_mode(windowed_size, flags)
        pygame.display.set_caption("BrickTok")
        # If game exists in outer scope, update its screen reference
        try:
            game.setScreen(screen)
        except Exception:
            pass

    # Initialize display
    screen = None
    set_display_mode(True)

    game = Game()
    game.setScreen(screen)
    game.start()

    clock = pygame.time.Clock()
    # Attach the clock to the game so the game can display FPS
    game.clock = clock

    while game.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()
            # Toggle FPS overlay with F3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                game.toggle_fps_display()

        game.update()
        game.render()

        pygame.display.flip()
        # Ensure fps_limit is a positive integer
        fps = int(game.fps_limit) if getattr(game, 'fps_limit', 60) else 60
        if fps <= 0:
            fps = 60
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
