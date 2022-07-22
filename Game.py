import asyncio
import threading
import pygame
import sys
from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape
from Globals import WIDTH, HEIGHT, FPS
from Server import startServer


def startGame():

    pygame.init()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    FramePerSec = pygame.time.Clock()

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    physics = PhysicsEngine()
    spawner = Spawner()
    inputHandler = InputHandler()

    while True:

        displaysurface.fill((0, 0, 0))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)

        newShape = spawner.handle()

        if(newShape):
            all_sprites.add(newShape)

        physics.update(all_sprites)
        inputHandler.handle()

        for event in pygame.event.get():
            if event.type == pygame.event.custom_type() - 1:
                print(str(event))
                shap = Shape()
                shap.randomize()
                all_sprites.add(shap)

        # let pygame handle events we don't process
        pygame.event.pump()


threads = []

thread = threading.Thread(target=startGame, args=())
thread.start()

asyncio.run(startServer())
