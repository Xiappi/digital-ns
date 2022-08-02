from turtle import shape
import pygame
import random
from pygame.math import Vector2 as vec
from Globals import WIDTH, HEIGHT

ACC = 5

WHITE = (255, 255, 255)


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 30

        self.surf = pygame.Surface((self.width, self.width))

        self.height = self.width
        self.width = self.width

        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))

        self.surf.fill(self.color)
        self.image = self.surf
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.pos = vec((200, 200))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.friction = -0.12

        self.rect = pygame.draw.circle(
            self.image, self.color, (self.width//2, self.height//2), self.radius)

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
