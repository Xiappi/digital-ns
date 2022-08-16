from Shape import Shape
import pygame

class YourShape(Shape):

    # def drawMe(self, canvas, camera):
    #      return pygame.draw.rect(canvas, self.color, pygame.Rect(self.pos.x - camera.offset.x, self.pos.y - camera.offset.y, 25,25))
         
    def __init__(self) -> None:
        super().__init__()
        self.drawLambda =  self.drawMe

