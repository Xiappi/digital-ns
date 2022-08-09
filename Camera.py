from abc import ABC, abstractmethod
from pygame.math import Vector2 as vec
import Globals

class Camera:
    def __init__(self, obj) -> None:
        self.object = obj
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.CONST = vec(-Globals.WINDOW_WIDTH / 2 , -Globals.WINDOW_HEIGHT/2)

    def setMethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera, obj) -> None:
        self.camera = camera
        self.object = obj

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):

    def __init__(self, camera, obj) -> None:
        super().__init__(camera, obj)

    def scroll(self):
        self.camera.offset_float.x += (self.object.rect.x -self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.object.rect.y -self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(CamScroll):
    def __init__(self, camera, obj):
        super().__init__(self, camera, obj)

    def scroll(self):


        self.camera.offset_float.x += (self.object.rect.x -self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.object.rect.y -self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, Globals.ARENA_WIDTH - self.camera.DISPLAY_W)