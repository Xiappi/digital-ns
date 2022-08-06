import asyncio
from tkinter import EventType
import pygame
import websockets
import EventTypes

async def server(websocket):
    data = await websocket.recv()
    print(f"<<< {data}")

    greeting = f"Hello: {data}!"

    pygame.event.post(pygame.event.Event(
        EventTypes.GREETING, message=greeting))

    events = pygame.event.get(EventTypes.SHAPES)

    for event in events:
        for shape in event.shapes:
            await websocket.send(f"{shape.pos.x},{shape.pos.y}")


async def startServer():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":

    asyncio.run(startServer())
