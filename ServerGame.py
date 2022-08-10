import asyncio
import threading
import pygame
import sys

import EventTypes

from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape
from Globals import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from Server import main


def startGame():

    pygame.init()

    displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Server")
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

        for event in pygame.event.get(EventTypes.GREETING):
            print(str(event))
            shap = Shape()
            shap.randomize()
            all_sprites.add(shap)

        # Now post all of the current shapes
        pygame.event.post(pygame.event.Event(
            EventTypes.SHAPES, shapes=all_sprites
        ))

        # let pygame handle events we don't process
        pygame.event.pump()



if __name__ == "__main__":
    
    threads = []

    thread = threading.Thread(target=startGame, args=())
    thread.start()

    asyncio.run(main())
