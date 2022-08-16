from Shape import Shape
from pygame.math import Vector2 as vec
import pygame

class YourShape(Shape):

    # def drawMe(self, canvas, camera):
    #      return pygame.draw.rect(canvas, self.color, pygame.Rect(self.pos.x - camera.offset.x, self.pos.y - camera.offset.y, 25,25))
         
    def __init__(self) -> None:
        super().__init__()
        self.drawLambda =  self.drawMe

        self.name = "Zac"

        self.color = (0, 0, 0)

        self.acc = vec(5, 5)

        self.radius = 5

        self.pos = vec((0, 0))
