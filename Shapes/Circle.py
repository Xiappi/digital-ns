from Shape import Shape

import pygame


class Circle(Shape):

    def __init__(self):
        super().__init__(self)
        self.radius = 10
        self.rect = pygame.draw.circle(
            self.image, self.color, (self.width//2, self.height//2), self.radius)
