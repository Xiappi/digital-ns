
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

        canvas.blit(background, (ARENA_OFFSET - camera.offset.x - ARENA_WIDTH/2, ARENA_OFFSET - camera.offset.y - ARENA_HEIGHT/2)) 


        for entity in all_sprites:
            canvas.blit(entity.surf, (entity.rect.x - camera.offset.x, entity.rect.y - camera.offset.y))

        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(ARENA_OFFSET - camera.offset.x, ARENA_OFFSET - camera.offset.y , ARENA_WIDTH - ARENA_OFFSET, ARENA_HEIGHT - ARENA_OFFSET),  2)
        
        # ALWAYS DRAW CANVAS ON WINDOW LAST
        window.blit(canvas, (0,0))
        print(camera.offset)

threads = []

thread = threading.Thread(target=startGame, args=())
thread.start()

# asyncio.run(Server.startServer())