"""Test script to quickly test the score screen"""
import pygame
import sys
sys.path.insert(0, '.')

from src.ScoreScreen import ScoreScreen

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Score Screen Test")
clock = pygame.time.Clock()

# Create score screen with P1 winning 10-7
score_screen = ScoreScreen("P1", 10, 7)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        score_screen.handle_event(event)
    
    result = score_screen.update()
    if result:
        print(f"Result: {result}")
        running = False
    
    score_screen.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Test complete!")
