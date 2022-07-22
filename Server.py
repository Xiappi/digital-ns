import asyncio
import pygame
import websockets


async def server(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    pygame.event.post(pygame.event.Event(
        pygame.event.custom_type(), message=greeting))

    await websocket.send(greeting)


async def startServer():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":

    asyncio.run(startServer())
