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

        if len(pygame.event.get(pygame.WINDOWMOVED)) > 0:
            all_sprites.empty()
            pygame.event.pump()
            continue

        displaysurface.fill((0, 0, 0))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)

        for event in pygame.event.get(EventTypes.CREATE_SHAPE):
            for shape in str(event.shapes).split(";"):
                alreadyExists = False
                
                try:
                    name = str(shape.split(",")[0])
                    xPos = int(shape.split(",")[1])
                    yPos = int(shape.split(",")[2])
                    radi = int(shape.split(",")[3])
                except:
                    continue

                # Check all existing shapes to make sure there isn't one already with the same UUID
                for shape2 in all_sprites:
                    # If the shape already exists
                    if shape2.name == name:
                        alreadyExists = True
                        shape2.pos.x = xPos
                        shape2.pos.y = yPos
                        shape2.radius = radi
                        shap.move()

                # If the shape doesn't exist
                if (alreadyExists == False or len(all_sprites) == 0):
                    shap = Shape(name, xPos, yPos, radi)
                    shap.move()
                    all_sprites.add(shap)

        # let pygame handle events we don't process
        pygame.event.pump()


if __name__ == "__main__":

    # having the game in a different thread is why we need to close game and asyncio separately
    threads = []

    thread = threading.Thread(target=startGame, args=())
    thread.start()

    asyncio.run(handleClient())
