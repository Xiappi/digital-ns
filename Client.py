import asyncio
import websockets
import EventTypes
import pygame

async def handleClient():
    reader, writer = await asyncio.open_connection(
        'localhost', 8888)


    # read while we server is up
    while not reader.at_eof():
        data = await reader.read(50)
        print(f'Received: {data.decode()!r}')

        shapeStr = data.decode()

        pygame.event.post(pygame.event.Event(
        EventTypes.CREATE_SHAPE, shapes=shapeStr))

        # TODO: check for exit input to stop gracefully
    print("client exiting")

if __name__ == "__main__":
    asyncio.run(handleClient())