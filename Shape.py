from turtle import shape
from uuid import uuid4
import pygame
import random
from pygame.math import Vector2 as vec
from Globals import *

ACC = 5
WHITE = (255, 255, 255)


class Shape(pygame.sprite.Sprite):
    def __init__(self, name=uuid4(), x=-1, y=-1, radius=-1):
        super().__init__()

        self.name = name
        
        if(radius == -1):
            self.radius = random.randint(5, 10)
        else:
            self.radius = radius
        
        self.height = self.radius * 2
        self.width = self.radius * 2

        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = (255, 0, 0)

        self.surf = pygame.Surface((self.height, self.width))
        self.surf.fill(self.color) 

        self.image = self.surf
        self.image.fill(WHITE)    
        self.image.set_colorkey(WHITE)  

        if (x == -1):
            xPos = 200
        else:
            xPos = x
        if (y == -1):
            yPos = 200
        else:
            yPos = y

        self.pos = vec((xPos, yPos))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.friction = -0.12

        self.rect = pygame.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.radius)

    def move(self):

        self.vel += self.acc

        self.acc.x = self.acc.x * self.friction
        self.acc.y = self.acc.y * self.friction

        # self.vel += self.acc
        self.pos += self.vel

        if self.pos.x + self.getBound() >= ARENA_WIDTH or self.pos.x - self.getBound() <= ARENA_OFFSET:
            self.acc.x = -self.acc.x
            self.vel.x = -self.vel.x

        if self.pos.y + self.getBound() >= ARENA_HEIGHT or self.pos.y - self.getBound() <= ARENA_OFFSET:
            self.acc.y = -self.acc.y
            self.vel.y = -self.vel.y

        self.rect.center = self.pos

    def randomize(self):
        self.acc.x = -ACC * random.random()
        self.acc.y = -ACC * random.random()

    def getBound(self):
        return self.radius

    def redraw(self):
        self.height = self.radius * 2
        self.width = self.radius * 2
        self.surf = pygame.Surface((self.height, self.width))
        self.image = self.surf

        # Make sure that when it's redrawn, it's kept in bounds
        self.rect = pygame.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.radius)


        self.rect = pygame.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.radius)
