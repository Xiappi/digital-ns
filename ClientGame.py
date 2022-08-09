import asyncio
import threading
from tkinter import EventType
import pygame
import sys

import EventTypes

from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape
from Globals import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from Client import hello


def startGame():

    pygame.init()

    displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Client")
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

        #all_sprites.empty()

        for event in pygame.event.get(EventTypes.CREATE_SHAPE):
            print(str(event))
            shap = Shape()
            shap.randomize()
            shap.pos.x = float(event.coords[0])
            shap.pos.y = float(event.coords[1])
            all_sprites.add(shap)

        # let pygame handle events we don't process
        pygame.event.pump()


threads = []

thread = threading.Thread(target=startGame, args=())
thread.start()

asyncio.run(hello())
