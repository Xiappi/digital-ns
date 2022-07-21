import pygame
from Shape import Shape


class Spawner():

    def __init__(self) -> None:
        pass

    def handle(self):

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                shape = Shape()
                shape.randomize()
                return shape
