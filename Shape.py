from uuid import uuid4

import pygame
import random
from pygame.math import Vector2 as vec
from Globals import *
import ShapeTypes

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

        self.shapeType = ShapeTypes.CIRCLE         
        
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
        
        drawnShape = None

        if self.shapeType == ShapeTypes.SQUARE:
            drawnShape = pygame.draw.rect(canvas, self.color, pygame.Rect(self.pos.x - camera.offset.x, self.pos.y - camera.offset.y, self.radius,self.radius))
        elif self.shapeType == ShapeTypes.TRIANGLE:
            bottomLeft = (self.pos.x - camera.offset.x, self.pos.y - camera.offset.y)
            bottomRight = (self.pos.x - camera.offset.x, self.pos.y - camera.offset.y + self.radius)
            middleTop =  (self.pos.x - camera.offset.x - self.radius, self.pos.y - camera.offset.y + self.radius)

            pygame.draw.polygon(canvas, self.color, points=[bottomLeft, bottomRight, middleTop])
            
        else: 
            drawnShape = pygame.draw.circle(canvas, self.color, (self.pos.x - camera.offset.x, self.pos.y - camera.offset.y), self.radius)
        self.rect = drawnShape
         

        
    