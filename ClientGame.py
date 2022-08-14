import asyncio
import threading
import pygame
import sys

import EventTypes

from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape
from Globals import *
from Client import handleClient

def startGame():
    isRunning = True
    pygame.init()

    displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Client")
    FramePerSec = pygame.time.Clock()

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    physics = PhysicsEngine()
    spawner = Spawner()
    inputHandler = InputHandler()

    while isRunning:

        if pygame.event.get(eventtype=pygame.QUIT):
            isRunning = False
            pygame.quit()
            sys.exit()

        displaysurface.fill((0, 0, 0))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)

        all_sprites.empty()

        for event in pygame.event.get(EventTypes.CREATE_SHAPE):
            for shape in str(event.shapes).split(";"):
                try:
                    name = str(shape.split(",")[0])
                    xPos = int(shape.split(",")[1])
                    yPos = int(shape.split(",")[2])
                    radi = int(shape.split(",")[3])

                    shap = Shape(name, xPos, yPos, radi)
                    shap.move()
                    all_sprites.add(shap)
                except:
                    continue

        #physics.update(all_sprites)

        # let pygame handle events we don't process
        pygame.event.pump()


if __name__ == "__main__":

    # having the game in a different thread is why we need to close game and asyncio separately
    threads = []

    thread = threading.Thread(target=startGame, args=())
    thread.start()

    asyncio.run(handleClient())
