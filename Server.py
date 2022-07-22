import asyncio
import websockets

async def server(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def startServer():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # run forever
        