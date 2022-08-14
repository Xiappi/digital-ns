import asyncio
from http import client
import websockets
import EventTypes
import pygame

async def handleClient():
    reader, writer = await asyncio.open_connection(
        'localhost', 8888)

    writer.write("hi".encode())

    # read while we server is up
    while not reader.at_eof():
        data = await reader.read(500)
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