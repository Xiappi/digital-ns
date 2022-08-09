import asyncio
import websockets
import pygame

import EventTypes


async def client(websocket):
    name = "Ping"
    await websocket.send(name)

    coords = await websocket.recv()
    print(f"<<< {coords}")

    x = str(coords).split(",")[0]
    y = str(coords).split(",")[1]

    pygame.event.post(pygame.event.Event(
    EventTypes.CREATE_SHAPE, coords=(x, y)))

async def hello():
    uri = "ws://localhost:8765"

    async for websocket in websockets.connect(uri):
        try:
            await client(websocket)
        except websocket.ConnectionClosed:
            continue

if __name__ == "__main__":

    asyncio.run(hello())
