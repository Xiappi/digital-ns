import asyncio
import logging
import threading
import time
import concurrent.futures
from ServerGame import startGame
from Server import startServer


def test():
    asyncio.run(startServer())


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    # threads.append(threading.Thread(target=startGame, args=()))
    threads.append(threading.Thread(target=startServer, args=()))

    for thread in threads:
        thread.start()
