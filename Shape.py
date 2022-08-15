from turtle import shape
from uuid import uuid4
import pygame
import random
from pygame.math import Vector2 as vec
from Globals import *

ACC = 5
WHITE = (255, 255, 255)


class Shape(pygame.sprite.Sprite):
    def __init__(self, name="Default Name", uuid=0, x=-1, y=-1, radius=-1):
        super().__init__()

        self.name = name

        self.color = (255, 0, 0)
        self.rect = None

        if uuid == 0:
            self.uuid = uuid4()
        else:
            self.uuid = uuid
        
        if(radius == -1):
            self.radius = random.randint(5, 10)
        else:
            self.radius = radius
        
        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
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


        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.text = self.font.render(self.name, True, (255, 255, 255), None)
        self.textRect = self.text.get_rect()
        

    def __str__(self):
        return f"{self.uuid},{round(self.pos.x)},{round(self.pos.y)},{self.radius}"

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

        

    def randomize(self):
        self.acc.x = -ACC * random.random()
        self.acc.y = -ACC * random.random()

    def getBound(self):
        return self.radius

    def draw(self, canvas, camera):
        self.rect = pygame.draw.circle(canvas, self.color, (self.pos.x - camera.offset.x, self.pos.y - camera.offset.y), self.radius)
        self.textRect.center = (self.pos.x - camera.offset.x, self.pos.y - camera.offset.y + 25 + self.radius)
        canvas.blit(self.text, self.textRect)
        
        


