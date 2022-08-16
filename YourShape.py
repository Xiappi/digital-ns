from Shape import Shape
from pygame.math import Vector2 as vec
import pygame

class YourShape(Shape):

    # def drawMe(self, canvas, camera):
    #      return pygame.draw.rect(canvas, self.color, pygame.Rect(self.pos.x - camera.offset.x, self.pos.y - camera.offset.y, 25,25))
         
    def __init__(self) -> None:
        super().__init__()
        self.drawLambda =  self.drawMe

        # The Name of your shape
        self.name = "Zac"

        # The color of your shape
        # (Red, Blue, Green)
        self.color = (0, 0, 0)

        # How fast your shape is
        self.acc = vec(5, 5)

        # How big yuour shape is
        self.radius = 5

        # Where your shape in the game
        self.pos = vec((0, 0))
