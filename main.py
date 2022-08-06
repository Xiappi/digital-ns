from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
from turtle import back, window_height
import pygame
import sys
import Server
import threading
import asyncio
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
import Shape
from Globals import *

import Camera

def startGame():
    background = pygame.image.load("Images/background.jpg")
    border = pygame.Rect(0, 0, ARENA_WIDTH, ARENA_HEIGHT)
    isRunning = True    
    
    pygame.init()

    canvas = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    pygame.display.set_caption("Game")
    FramePerSec = pygame.time.Clock()

    physics = PhysicsEngine()
    spawner = Spawner()

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    myShape = Shape.Shape()
    camera = Camera.Camera(myShape)
    follow = Camera.Follow(camera, myShape)
    camera.setMethod(follow)

    myShape.randomize()
    # myShape.vel.x = 10
    # myShape.vel.y = 10
    # myShape.pos.x = 0
    # myShape.pos.y = 0

    
    all_sprites.add(myShape)

    while isRunning:

        if pygame.event.get(eventtype=pygame.QUIT):
            isRunning = False
            Server.isRunning2 = False
            pygame.quit()
            sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)

        newShape = spawner.handle()

        if(newShape):
            all_sprites.add(newShape)

        physics.update(all_sprites)

        # let pygame handle events we don't process
        pygame.event.pump()

        camera.scroll()

        ### HANDLE DRAWING ###
        canvas.fill((0,0,0))
        window.fill((0, 0, 0))

        # canvas.blit(background, (camera.offset.x - ARENA_WIDTH/2, camera.offset.y - ARENA_HEIGHT/2))
        canvas.blit(background, (camera.offset.x - ARENA_WIDTH/2, camera.offset.y - ARENA_HEIGHT/2))
    
        for entity in all_sprites:
            canvas.blit(entity.surf, (entity.rect.x - camera.offset.x, entity.rect.y - camera.offset.y))

        # pygame.draw.rect(canvas, (255,0,0), pygame.Rect(camera.offset.x - ARENA_WIDTH/2, camera.offset.y - ARENA_HEIGHT/2, ARENA_WIDTH, ARENA_HEIGHT),  2)
        
        # ALWAYS DRAW CANVAS ON WINDOW LAST
        window.blit(canvas, (0,0))

threads = []

thread = threading.Thread(target=startGame, args=())
thread.start()

# asyncio.run(Server.startServer())