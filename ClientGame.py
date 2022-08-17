import asyncio
from pydoc import cli
import threading
import pygame
import sys
import EventTypes
from uuid import UUID
from Shape import Shape
import Globals
from Client import handleClient
import Camera
from YourShape import YourShape

def createShape():
    yourShape = YourShape()
    return yourShape

def startGame(loop):
    # INITIALIZATION STUFF

    pygame.init()

    background = pygame.image.load("Images/background.jpg")

    canvas = pygame.Surface((Globals.WINDOW_WIDTH,Globals.WINDOW_HEIGHT))
    window = pygame.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))

    pygame.display.set_caption("Client")

    FramePerSec = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 24)

    # CREATE SHAPE GROUP
    all_sprites = pygame.sprite.Group()

    camera = Camera.Camera()
    follow = Camera.Follow(camera)
    camera.setMethod(follow)

    # CREATE CLIENT SHAPE AND SEND AS EVENT, SO WE KNOW WHICH ONE WE CREATED ORIGINALLY
    clientShape = createShape()
    camera.setObjectToFollow(clientShape)
    print("create vent")
    pygame.event.post(pygame.event.Event(
        EventTypes.CLIENT_CREATE_SHAPE, shape=clientShape
    ))
    
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
        
        pygame.display.update()
        FramePerSec.tick(Globals.FPS)

        events = pygame.event.get(EventTypes.SERVER_SEND_SHAPE)

        # no events mean nothing to draw
        if len(events) > 0:
            shapes = events[0].shapes

            # clear out existing shapes before we add new ones
            all_sprites.empty()
            for shape in shapes:
                all_sprites.add(shape)
                if shape.uuid == clientShape.uuid:
                    camera.setObjectToFollow(shape)

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


if __name__ == "__main__":
    Globals.init()
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=startGame, args=(loop,), daemon=True)
    thread.start()

    asyncio.run(handleClient())
