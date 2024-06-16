import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

class DynamicText():
    def __init__(self, text:str, x:float, y:float, fontPath:str, size:int, color):
        self.screen = pg.display.get_surface()
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.relativeSize = size / W
        self.x = x
        self.y = y
        self.size = size
        self.fontPath = fontPath
        self.text = text
        self.color = color

        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def resize(self, W:int, H:int):
        self.x = self.relativeX * W
        self.y = self.relativeY * H
        self.size = int(self.relativeSize * W)
        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def changeText(self, text):
        self.text = text
        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def render(self):
        self.screen.blit(self.renderText, (self.x, self.y))

class DynamicImage():
    def __init__(self, x, y, ObjectScale, image:pg.Surface, manager, rotate = 0):
        self.screen = pg.display.get_surface()
        self.manager = manager
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.x = x
        self.y = y
        self.rotate = rotate
        self.imageSave = image
        self.scale = ObjectScale / W
        
        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * W)

        self.interpolationEnd = False

    def resize(self, W, H):
        self.x = self.relativeX * W
        self.y = self.relativeY * H
        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * W)

    def interpolationX(self, X1, X2):
        W = 1280
        H = 720
        if not self.interpolationEnd: self.relativeX = self.x +1 / W

    def render(self):
        self.screen.blit(self.image, (self.x, self.y))

class DynamicInput():
    def __init__(self, x, y, ObjectW, ObjectH, fontPath:str, size:int, color, manager, defaultText=""):
        self.screen = pg.display.get_surface()
        self.manager = manager
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.x = x
        self.y = y
        self.relativeW = ObjectW / W
        self.relativeH = ObjectH / H
        self.element = pgu.elements.UITextEntryLine(
            relative_rect=pg.Rect((self.x, self.y), (ObjectW, ObjectH)),
            manager=self.manager,
            placeholder_text=defaultText
        )
    def resize(self, W, H):
        self.element.set_dimensions((self.relativeW * W, self.relativeH * H))
        self.element.set_position((self.relativeX * W, self.relativeY * H))

class DynamicButton():
    def __init__(self, x, y, ObjectW, ObjectH, text, manager, ids = ObjectID("","")):
        self.screen = pg.display.get_surface()
        self.manager = manager
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.x = x
        self.y = y
        self.relativeW = ObjectW / W
        self.relativeH = ObjectH / H
        self.element = pgu.elements.UIButton(
            relative_rect=pg.Rect((self.x, self.y), (ObjectW, ObjectH)),
            text=text,
            object_id=ids,
            manager=self.manager
        )

    def resize(self, W, H):
        self.element.set_relative_position((self.relativeX * W, self.relativeY * H))
        self.element.set_dimensions((self.relativeW * W, self.relativeH * H))