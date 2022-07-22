import pygame
import random
from pygame.math import Vector2 as vec
from Globals import WIDTH, HEIGHT

ACC = 5
SHAPE_WIDTH = 30


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((SHAPE_WIDTH, SHAPE_WIDTH))

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = vec((200, 200))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.friction = -0.12

    def move(self):

        self.vel += self.acc

        self.acc.x = self.acc.x * self.friction
        self.acc.y = self.acc.y * self.friction

        # self.vel += self.acc
        self.pos += self.vel

        if self.pos.x + self.getBound() >= WIDTH or self.pos.x - self.getBound() <= 0:
            self.acc.x = -self.acc.x
            self.vel.x = -self.vel.x

        if self.pos.y + self.getBound() >= HEIGHT or self.pos.y - self.getBound() <= 0:
            self.acc.y = -self.acc.y
            self.vel.y = -self.vel.y

        self.rect.midbottom = self.pos

    def randomize(self):
        self.acc.x = -ACC * random.random()
        self.acc.y = -ACC * random.random()

    def getBound(self):
        return SHAPE_WIDTH
