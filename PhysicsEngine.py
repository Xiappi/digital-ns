import pygame

class PhysicsEngine():

    def __init__(self):
        pass

    def update(self, shapeGroup):
        for shape1 in shapeGroup:
            for shape2 in shapeGroup:
                if shape1 != shape2:
                    if pygame.sprite.collide_rect(shape1, shape2):

                        consume(shape1, shape2)

            shape1.move()


def consume(shape1, shape2):
    if shape1.radius > shape2.radius:
        shape1.radius += shape2.radius
        shape1.redraw()
        shape2.kill()
    elif shape2.radius > shape1.radius:
        shape2.radius += shape1.radius
        shape2.redraw()
        shape1.kill()
    else:
        bounce(shape1, shape2)

def bounce(shape1, shape2):

    # 0,0 is top left
    #If Shape one is more to the left than shape 2
    if shape1.pos.x < shape2.pos.x:
        # Shape 1 Go left
        shape1.acc.x = -abs(shape1.acc.x)
        shape1.vel.x = -abs(shape1.vel.x)
        # Shape 2 go right
        shape2.acc.x = abs(shape2.acc.x)
        shape2.vel.x = abs(shape2.vel.x)
    else:
        # Shape 1 Go right
        shape1.acc.x = abs(shape1.acc.x)
        shape1.vel.x = abs(shape1.vel.x)
        # Shape 2 go left
        shape2.acc.x = -abs(shape2.acc.x)
        shape2.vel.x = -abs(shape2.vel.x)
    
    if shape1.pos.y < shape2.pos.y:
        # Shape 1 Go down
        shape1.acc.y = -abs(shape1.acc.y)
        shape1.vel.y = -abs(shape1.vel.y)
        # Shape 2 go up
        shape2.acc.y = abs(shape2.acc.y)
        shape2.vel.y = abs(shape2.vel.y)
    else:
        # Shape 1 Go up
        shape1.acc.y = abs(shape1.acc.y)
        shape1.vel.y = abs(shape1.vel.y)
        # Shape 2 go down
        shape2.acc.y = -abs(shape2.acc.y)
        shape2.vel.y = -abs(shape2.vel.y)
