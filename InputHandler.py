from multiprocessing import Event
import pygame
import sys


class InputHandler():

    def __init__(self) -> None:
        pass

    def handle(self):
        if pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()
