import pygame
import sys
import Server
import threading
import asyncio
from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape
from Globals import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def startGame():

    pygame.init()

    displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
        x = inputHandler.handle()

        # let pygame handle events we don't process
        pygame.event.pump()

threads = []

thread = threading.Thread(target=startGame, args=())
thread.start()

asyncio.run(Server.startServer())