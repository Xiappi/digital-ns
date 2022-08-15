import asyncio
from http import client
import websockets
import EventTypes
import pygame
import Globals

async def handleClient():
    pygame.init()
    
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)


    # read while we server is up
    while not reader.at_eof() and Globals.IS_RUNNING:
            
        data = await reader.read(5000)
        print(f'Received: {data.decode()!r}')

        shapeStr = data.decode()
        pygame.event.post(pygame.event.Event(
        EventTypes.SERVER_SEND_SHAPE, shapes=shapeStr))

        # clientShapeEvents = pygame.event.get(EventTypes.CLIENT_SEND_SHAPE)
        # # If there is a shape to send back
        # try:
        #     shape = clientShapeEvents[0].shape
        #     sendShapeStr = (f"{shape.name},{round(shape.pos.x)},{round(shape.pos.y)},{shape.radius}")
        #     writer.write(f"{sendShapeStr}".encode())
        # except:
        #     continue

        # TODO: check for exit input to stop gracefully
    print("client exiting")

if __name__ == "__main__":
    asyncio.run(handleClient())