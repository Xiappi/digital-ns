import asyncio
import pygame
import EventTypes
from Shape import Shape
import Globals

connections = set()
backgroundTasks = set()

async def handleServer(reader, writer):

    # data = await reader.read(500)
    # createShape(data)

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
    pygame.init()
    # TODO: exit on some condition 
    while Globals.IS_RUNNING:

        events = pygame.event.get(eventtype=EventTypes.SHAPES)
        try:
            event = events[0]
        except IndexError:
            pass

        for connection in connections:
            
            try:
                addr = connection.get_extra_info('peername')
                print(f"saying hi to {addr}")
                # connection.write("hi".encode())
                # await connection.drain()
                shapeStr = ""

                for shape in event.shapes:
                    shapeStr += (f"{shape.name},{round(shape.pos.x)},{round(shape.pos.y)},{shape.radius}")
                    shapeStr += ";" 

                connection.write(f"{shapeStr}".encode())
                connection.drain()

                # connection.write(f"{shapeStr}".encode())
            except Exception as e:
                print(f"error with {connection.get_extra_info('peername')}")
                print(e)


        await asyncio.sleep(.03)

def createShape(data):
    pygame.event.post(EventTypes.CLIENT_SEND_SHAPE, shape=Shape())


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

    async with server:
        await server.start_serving()
        while Globals.IS_RUNNING:
            await asyncio.sleep(0.5)
                
if __name__ == "__main__":
    asyncio.run(main())
