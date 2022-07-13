import pygame

pygame.init()

# CONSTANTS

HEIGHT = 640
WIDTH = 480
ACC = 0.5
FRIC = -0.12
FPS = 60


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    pygame.display.update()

pygame.quit()
