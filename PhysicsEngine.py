import pygame

class PhysicsEngine():

    def __init__(self):
        pass

    def update(self, shapeGroup):
        for shape1 in shapeGroup:
            for shape2 in shapeGroup:
                if shape1 != shape2:
                    if pygame.sprite.collide_rect(shape1, shape2):
                        
                        #TODO: Determine the direction of each shape based on their current direction
                        shape1.acc.x = -shape1.acc.x
                        shape1.vel.x = -shape1.vel.x
                        shape2.acc.x = -shape2.acc.x
                        shape2.vel.x = -shape2.vel.x

            shape1.move()
