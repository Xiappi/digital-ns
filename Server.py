import asyncio
import pickle
import pygame
import EventTypes
from Shape import Shape
import Globals

connections = set()
backgroundTasks = set()

async def handleServer(reader, writer):

    addr = writer.get_extra_info('peername')

    try:
        data = await reader.read(10000)
        createShape(data)
    except Exception as e:
        print(f"Failed to get shape from {addr}")

    connections.add(writer)

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
    pygame.init()
    # TODO: exit on some condition 
    while Globals.IS_RUNNING:
        await asyncio.sleep(.03)

        events = pygame.event.get(eventtype=EventTypes.SHAPES)

        if len(events) == 0:
            continue
        
        event = events[0]

        for i in range(len(connections) -1):
            
            try:
                connection = connections[i]
                shapeList = pickle.dumps(event.shapes)
                connection.write(shapeList)
                await connection.drain()

            except Exception as e:
                print(f"error with {connection.get_extra_info('peername')}")
                print(e)


def createShape(data):
    receivedShape = pickle.loads(data)
    pygame.event.post(pygame.event.Event(
        EventTypes.CLIENT_SEND_SHAPE, shape=receivedShape))


async def main():

    # initiate data sending and cleanup after it finishes
    sendTask = asyncio.create_task(handleSending())
    sendTask.add_done_callback(backgroundTasks.discard)
    
    backgroundTasks.add(sendTask)

    # start server
    server = await asyncio.start_server(
        handleServer, Globals.IP, 8888)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.start_serving()
        while Globals.IS_RUNNING:
            await asyncio.sleep(0.5)
                
if __name__ == "__main__":
    Globals.init()
    asyncio.run(main())
