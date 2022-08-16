import asyncio
from ctypes import sizeof
from http import client
import pickle
import EventTypes
import pygame
import Globals
from YourShape import YourShape




async def handleClient():
    pygame.init()
    
    try:
        reader, writer = await asyncio.open_connection(
            Globals.IP, 8888)
    except ConnectionRefusedError:
        print("Server is not open")
        print("Closing Client...")
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return

    print("checke vent")

    
    attempts = 0

    while attempts < 3:
        # GET YOUR SHAPE AND SEND TO SERVRE
        clientShapeEvent = pygame.event.get(EventTypes.CLIENT_CREATE_SHAPE)
        print(clientShapeEvent)
        if len(clientShapeEvent) > 0:

            data = pickle.dumps(clientShapeEvent[0].shape)
            writer.write(data)
            await writer.drain()
            break
        
        attempts+=1
        await asyncio.sleep(0.5)

    # read while we server is up
    while not reader.at_eof() and Globals.IS_RUNNING:
        try:
            data = await reader.read(100000)
            shapes = pickle.loads(data)
            pygame.event.post(pygame.event.Event(
            EventTypes.SERVER_SEND_SHAPE, shapes=shapes))
        except:
            Globals.IS_RUNNING == False
            break

        # TODO: check for exit input to stop gracefully
    print("client exiting")
    pygame.event.post(pygame.event.Event(pygame.QUIT))

if __name__ == "__main__":
    Globals.init()
    asyncio.run(handleClient())