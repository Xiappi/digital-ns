import pygame
import sys
from Shape import Shape
from Globals import WIDTH, HEIGHT, FPS


pygame.init()

# CONSTANTS


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FramePerSec = pygame.time.Clock()

# CREATE SHAPE
all_sprites = pygame.sprite.Group()

s1 = Shape()
all_sprites.add(s1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
    s1.move()
