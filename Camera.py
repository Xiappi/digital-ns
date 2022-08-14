from abc import ABC, abstractmethod
from pygame.math import Vector2 as vec
import Globals

class Camera:
    def __init__(self) -> None:
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.CONST = vec(-Globals.WINDOW_WIDTH / 2 , -Globals.WINDOW_HEIGHT/2)
        self.object = None

    def setObjectToFollow(self, obj):
        self.object = obj

    def setMethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera) -> None:
        self.camera = camera

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):

    def __init__(self, camera) -> None:
        super().__init__(camera)

    def scroll(self):
        if self.camera.object == None:
            return
        
        self.camera.offset_float.x += (self.camera.object.pos.x -self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.camera.object.pos.y -self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


