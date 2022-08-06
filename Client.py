import asyncio
import websockets
import pygame

import EventTypes


async def client(websocket):
    name = "adam"
    await websocket.send(name)
    print(f">>> {name} connected!")

    while True:
        try:
            coords = await websocket.recv()
            print(f"<<< {coords}")

            x = str(coords).split(",")[0]
            y = str(coords).split(",")[1]

            pygame.event.post(pygame.event.Event(
            EventTypes.CREATE_SHAPE, coords=(x, y)))
        except:
            continue

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await client(websocket)

if __name__ == "__main__":

    asyncio.run(hello())
