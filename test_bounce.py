"""Test script to verify ball bounce mechanics"""
import pygame
import sys
sys.path.insert(0, '.')

from src.Ball import Ball
from src.Raquette import Raquette

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create objects
ball = Ball()
ball.waiting = False
ball._start_time = pygame.time.get_ticks()
ball.velocity = [300, 0]  # Moving right
ball.rect.center = (400, 300)
ball.setPosition(ball.rect.topleft)

paddle = Raquette("P1")
paddle.rect.x = 600
paddle.rect.y = 250
paddle.setPosition(paddle.rect.topleft)

print(f"Initial ball velocity: {ball.velocity}")
print(f"Ball position: {ball.rect.center}")
print(f"Paddle position: {paddle.rect.center}")

# Simulate movement until collision
running = True
frame = 0
while running and frame < 300:  # 5 seconds at 60fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check collision
    if ball.rect.colliderect(paddle.rect):
        print(f"\nFrame {frame}: COLLISION DETECTED!")
        print(f"  Ball velocity before: {ball.velocity}")
        print(f"  Ball center: {ball.rect.center}")
        ball.bounce_paddle(paddle)
        print(f"  Ball velocity after: {ball.velocity}")
        print(f"  Ball center: {ball.rect.center}")
        running = False  # Stop after first bounce
    
    # Update ball
    ball.update()
    
    # Draw
    screen.fill((0, 0, 0))
    ball.render(screen)
    paddle.render(screen)
    pygame.display.flip()
    
    frame += 1
    clock.tick(60)

if frame >= 300:
    print("\nNo collision detected after 5 seconds")
    print(f"Final ball position: {ball.rect.center}")

pygame.quit()
print("\nTest complete!")
