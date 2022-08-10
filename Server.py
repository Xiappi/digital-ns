# import asyncio
# import pygame
# import websockets
# import EventTypes

# async def server(websocket):

#     print("hi")
#     websocket.send("poeops")
#     pygame.event.post(pygame.event.Event(
#         EventTypes.GREETING, message=greeting))

#     events = pygame.event.get(EventTypes.SHAPES)
#     print("events: " + str(events))
#     for event in events:
#         for shape in event.shapes:
#             await websocket.send(f"{shape.pos.x},{shape.pos.y}")


# async def startServer():
#     sev = await asyncio.start_server(server, 'localhost', 15555)
#     async with sev:
#         await sev.serve_forever()

#     # async with websockets.serve(server, "localhost", 8765):
#     #     await stop  # run forever

# if __name__ == "__main__":
#     asyncio.run(startServer())

import asyncio
import pygame

connections = set()
backgroundTasks = set()

async def handleServer(reader, writer):

    connections.add(writer)
    addr = writer.get_extra_info('peername')
    
    try:
        await writer.wait_closed()
    except Exception:
        print(f"{addr} ended")
    finally:
        print(f"Closing {addr}")
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()

        print(f"Removing {addr} from connections")
        connections.remove(writer)

async def handleSending():

    # TODO: exit on some condition 
    while True:
        for connection in connections:
            addr = connection.get_extra_info('peername')
            print(f"saying hi to {addr}")
            connection.write(f"hi {addr}".encode())
        await asyncio.sleep(.5)


async def main():

    # initiate data sending and cleanup after it finishes
    sendTask = asyncio.create_task(handleSending())
    sendTask.add_done_callback(backgroundTasks.discard)
    backgroundTasks.add(sendTask)

    # start server
    server = await asyncio.start_server(
        handleServer, '127.0.0.1', 8888)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    # server forever TODO: should probably finish when SIGFAULT is encountered
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
