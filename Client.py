import asyncio
from http import client
import websockets
import EventTypes
import pygame
import Globals

async def handleClient():
    pygame.init()
    
    try:
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
    except ConnectionRefusedError:
        print("Server is not open")
        print("Closing Client...")
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return

    writer.write("hi".encode())

    # read while we server is up
    while not reader.at_eof() and Globals.IS_RUNNING:
            
        try:
            data = await reader.read(100000)
        except ConnectionResetError:
            Globals.IS_RUNNING == False
            break
        # print(f'Received: {data.decode()!r}')

        shapeStr = data.decode()
        pygame.event.post(pygame.event.Event(
        EventTypes.SERVER_SEND_SHAPE, shapes=shapeStr))

        clientShapeEvents = pygame.event.get(EventTypes.CLIENT_SEND_SHAPE)
        # If there is a shape to send back
        try:
            shape = clientShapeEvents[0].shape
            sendShapeStr = (f"{str(shape)}")
            writer.write(f"{sendShapeStr}".encode())
        except:
            continue

        # TODO: check for exit input to stop gracefully
    print("client exiting")
    pygame.event.post(pygame.event.Event(pygame.QUIT))

if __name__ == "__main__":
    asyncio.run(handleClient())