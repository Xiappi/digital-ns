import pygame
from Shape import Shape


class Spawner():

    def __init__(self) -> None:
        self.counter = 1
        pass

    def handle(self):

        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                shape = Shape(name=f"Bot {self.counter}")
                self.counter+=1
                shape.randomize()
                return shape
