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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print("Move Left")
        if keys[pygame.K_RIGHT]:
            print("Move right")
        if keys[pygame.K_UP]:
            print("Move up")
        if keys[pygame.K_DOWN]:
            print("Move down")
