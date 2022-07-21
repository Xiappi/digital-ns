

class PhysicsEngine():

    def __init__(self):
        pass

    def update(self, shapeGroup):
        for shape in shapeGroup:
            shape.move()
