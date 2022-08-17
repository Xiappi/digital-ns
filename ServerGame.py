from ast import arg
import asyncio
import threading
import pygame
import sys
import random

import EventTypes

from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
import Shape
import Globals
import Server 

import Camera

def smallPoints(all_sprites):
    for i in range(Globals.STARTING_SHAPES):
        xPos = random.randint(5, Globals.ARENA_WIDTH - 5)
        yPos = random.randint(5, Globals.ARENA_HEIGHT - 5)
        shape = Shape.Shape(name="", x=xPos, y=yPos, radius=3)
        all_sprites.add(shape)

def startGame(loop):
    # INITIALIZATION STUFF

    pygame.init()

    background = pygame.image.load("Images/background.jpg")

    canvas = pygame.Surface((Globals.WINDOW_WIDTH,Globals.WINDOW_HEIGHT))
    window = pygame.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))

    pygame.display.set_caption("Server")
    FramePerSec = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 24)

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    physics = PhysicsEngine()
    spawner = Spawner()

    camera = Camera.Camera()
    follow = Camera.Follow(camera)
    camera.setMethod(follow)

    smallPoints(all_sprites)

    while Globals.IS_RUNNING:
        if pygame.event.get(eventtype=pygame.QUIT):
            Globals.IS_RUNNING = False
            loop.stop()
            loop.close()
            sys.exit()

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_r:
                for shape in all_sprites:
                    shape.kill()
                smallPoints(all_sprites)

        deleteEvents = pygame.event.get(EventTypes.SERVER_DELETE_SHAPE)
        for event in deleteEvents:
            for shape in all_sprites:
                if shape.uuid == event.shapeId:
                    shape.kill()

        pygame.display.update()
        FramePerSec.tick(Globals.FPS)

        # HANDLE EVENTS BEFORE DRAWING
        newShape = spawner.handle()
        if(newShape):
            all_sprites.add(newShape)

        for event in pygame.event.get(EventTypes.CLIENT_SEND_SHAPE):
            print(str(event))
            clientShape = event.shape
            clientShape.randomize()
            all_sprites.add(clientShape)

        physics.update(all_sprites)

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

        canvas.blit(background, (Globals.ARENA_OFFSET - camera.offset.x - Globals.ARENA_WIDTH/2, Globals.ARENA_OFFSET - camera.offset.y - Globals.ARENA_HEIGHT/2)) 

        for entity in all_sprites:
            entity.draw(canvas, camera)

            text = font.render(entity.name, True, (255, 255, 255), None)
            textRect = text.get_rect()
            textRect.center = (entity.pos.x - camera.offset.x, entity.pos.y - camera.offset.y + 25 + entity.radius)
            canvas.blit(text, textRect)

        # draw arena bounds
        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(Globals.ARENA_OFFSET - camera.offset.x, Globals.ARENA_OFFSET - camera.offset.y , Globals.ARENA_WIDTH - Globals.ARENA_OFFSET, Globals.ARENA_HEIGHT - Globals.ARENA_OFFSET),  2)
        
        FramePerSec.tick(Globals.FPS)

        # let pygame handle events we don't process
        pygame.event.pump()

        # ALWAYS DRAW CANVAS ON WINDOW LAST, THEN UPDATE
        window.blit(canvas, (0,0))
        pygame.display.update()


thread = None


async def main():
    
    loop = asyncio.get_running_loop()
    await loop.create_task(Server.main())


async def TryMe():
    while True:
        if Globals.IS_RUNNING:
            await asyncio.sleep(0.5)
            continue

if __name__ == "__main__":
    Globals.init()

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=startGame, args=(loop,), daemon=True)
    thread.start()

    asyncio.run(main())

