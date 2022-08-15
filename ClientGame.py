import asyncio
import threading
import pygame
import sys

import EventTypes

from uuid import UUID
from PhysicsEngine import PhysicsEngine
from Spawner import Spawner
from Shape import Shape

import Globals


from Client import handleClient
import Camera

def startGame(loop):
    # INITIALIZATION STUFF

    pygame.init()

    background = pygame.image.load("Images/background.jpg")

    canvas = pygame.Surface((Globals.WINDOW_WIDTH,Globals.WINDOW_HEIGHT))
    window = pygame.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))

    pygame.display.set_caption("Client")

    FramePerSec = pygame.time.Clock()

    # CREATE SHAPE
    all_sprites = pygame.sprite.Group()

    camera = Camera.Camera()
    follow = Camera.Follow(camera)
    camera.setMethod(follow)

    myShape = Shape()
    myShape.randomize()
    camera.setObjectToFollow(myShape)

    createdShape = False

    while Globals.IS_RUNNING:

        if pygame.event.get(eventtype=pygame.QUIT):
            Globals.IS_RUNNING = False
            loop.stop()
            loop.close()
            sys.exit()

        if len(pygame.event.get(pygame.WINDOWMOVED)) > 0:
            all_sprites.empty()
            pygame.event.pump()
            continue

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     if(createdShape == False):
        #         pygame.event.post(pygame.event.event_name(
        #             EventTypes.CLIENT_SEND_SHAPE, shape=Shape()
        #         ))

        pygame.display.update()
        FramePerSec.tick(Globals.FPS)

        for event in pygame.event.get(EventTypes.SERVER_SEND_SHAPE):
        
            # If we got more shapes than we already have
            # then something most have gotten killed
            # Wipe the board and start again
            if len(str(event.shapes).split(";")) - 1 != len(all_sprites):
                all_sprites.empty()

            for shape in str(event.shapes).split(";"):
                alreadyExists = False
                
                # If there isn't enough data for the shape don't draw it
                if len(shape.split(",")) < 4:
                    continue

                try:
                    name = str(shape.split(",")[0])
                    xPos = int(shape.split(",")[1])
                    yPos = int(shape.split(",")[2])
                    radi = int(shape.split(",")[3])
                except:
                    continue

                try:
                    UUID(name)
                except ValueError:
                    print("Invalid UUID")
                    continue

                # Check all existing shapes to make sure there isn't one already with the same UUID
                for shape2 in all_sprites:
                    # If the shape already exists
                    if shape2.name == name:
                        alreadyExists = True
                        shape2.pos.x = xPos
                        shape2.pos.y = yPos
                        shape2.radius = radi
                        shape2.move()

                # If the shape doesn't exist
                if (alreadyExists == False or len(all_sprites) == 0):
                    shap = Shape(name, xPos, yPos, radi)
                    shap.move()
                    all_sprites.add(shap)
                    camera.setObjectToFollow(shap)

        camera.scroll()

        ### HANDLE DRAWING ###
        canvas.fill((0,0,0))
        window.fill((0, 0, 0))

        canvas.blit(background, (Globals.ARENA_OFFSET - camera.offset.x - Globals.ARENA_WIDTH/2, Globals.ARENA_OFFSET - camera.offset.y - Globals.ARENA_HEIGHT/2)) 

        for entity in all_sprites:
            entity.draw(canvas, camera)

        # draw arena bounds
        pygame.draw.rect(canvas, (255,0,0), pygame.Rect(Globals.ARENA_OFFSET - camera.offset.x, Globals.ARENA_OFFSET - camera.offset.y , Globals.ARENA_WIDTH - Globals.ARENA_OFFSET, Globals.ARENA_HEIGHT - Globals.ARENA_OFFSET),  2)
    
        FramePerSec.tick(Globals.FPS)

        # let pygame handle events we don't process
        pygame.event.pump()

        # ALWAYS DRAW CANVAS ON WINDOW LAST, THEN UPDATE
        window.blit(canvas, (0,0))
        pygame.display.update()


if __name__ == "__main__":
    Globals.init()

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=startGame, args=(loop,), daemon=True)
    thread.start()

    asyncio.run(handleClient())
