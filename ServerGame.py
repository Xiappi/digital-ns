import asyncio
import threading
import pygame
import sys

import EventTypes

from InputHandler import InputHandler
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
import Shape
from Globals import *
import Server 

import Camera



def startGame():

    # INITIALIZATION STUFF

    background = pygame.image.load("Images/background.jpg")
    isRunning = True    

    pygame.init()

    canvas = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Server")
    FramePerSec = pygame.time.Clock()

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    physics = PhysicsEngine()
    spawner = Spawner()
    inputHandler = InputHandler()

    camera = Camera.Camera()
    follow = Camera.Follow(camera)
    camera.setMethod(follow)

    while isRunning:

        if pygame.event.get(eventtype=pygame.QUIT):
            isRunning = False
            pygame.quit()
            sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)

        newShape = spawner.handle()

        if(newShape):
            all_sprites.add(newShape)

        # HANDLE EVENTS BEFORE DRAWING
        newShape = spawner.handle()
        if(newShape):
            all_sprites.add(newShape)

        physics.update(all_sprites)
        inputHandler.handle()

        for event in pygame.event.get(EventTypes.CLIENT_SEND_SHAPE):
            print(str(event))
            all_sprites.add(event.shape)

        # Now post all of the current shapes
        pygame.event.post(pygame.event.Event(
            EventTypes.SHAPES, shapes=all_sprites
        ))

        ### HANDLE CAMERA ###
        biggestShape = None
        for shape in all_sprites:
            if  biggestShape == None or biggestShape.radius < shape.radius:
                biggestShape = shape

            if camera.object == None or camera.object != biggestShape:
                camera.setObjectToFollow(biggestShape)


        camera.scroll()

        
        ### HANDLE DRAWING ###
        canvas.fill((0,0,0))
        window.fill((0, 0, 0))

        canvas.blit(background, (ARENA_OFFSET - camera.offset.x - ARENA_WIDTH/2, ARENA_OFFSET - camera.offset.y - ARENA_HEIGHT/2)) 

        for entity in all_sprites:
            entity.draw(canvas, camera)

        # draw arena bounds
        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(ARENA_OFFSET - camera.offset.x, ARENA_OFFSET - camera.offset.y , ARENA_WIDTH - ARENA_OFFSET, ARENA_HEIGHT - ARENA_OFFSET),  2)
        
        FramePerSec.tick(FPS)

        # let pygame handle events we don't process
        pygame.event.pump()

        # ALWAYS DRAW CANVAS ON WINDOW LAST, THEN UPDATE
        window.blit(canvas, (0,0))
        pygame.display.update()




if __name__ == "__main__":
    
    threads = []

    thread = threading.Thread(target=startGame, args=())
    thread.start()

    asyncio.run(Server.main())