import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID
import math

class DynamicText():
    def __init__(self, x:float, y:float, text:str, fontPath:str, size:int, color):
        self.screen = pg.display.get_surface()
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.relativeSize = size / W

        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX  * screenW
        self.y = self.relativeY * screenH
        self.size = int(self.relativeSize * screenW)
        self.fontPath = fontPath
        self.text = text
        self.color = color

        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def resize(self):
        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.size = int(self.relativeSize * screenW)
        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def changeText(self, text):
        self.text = text
        self.renderText = pg.font.Font(self.fontPath, self.size).render(self.text, True, self.color)

    def changeCoord(self, x, y):
        W = 1280
        H = 720
        screenW, screenH = pg.display.get_surface().get_size()
        if x != None:
            self.relativeX = x / W
            self.x = self.relativeX * screenW
        if y != None:
            self.relativeY = y / H
            self.y = self.relativeY * screenH

    def render(self):
        self.screen.blit(self.renderText, (self.x, self.y))

class DynamicRect():
    def __init__(self, x, y, ObjectW, ObjectH, color):
        self.screen = pg.display.get_surface()
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H
        self.relativeW = ObjectW /self.W
        self.relativeH = ObjectH / self.H

        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.ObjectW = self.relativeW * screenW
        self.ObjectH = self.relativeH * screenH
        self.color = color

    def resize(self):
        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.ObjectW = self.relativeW * screenW
        self.ObjectH = self.relativeH * screenH

    def changeCoord(self, x, y):
        screenW, screenH = self.screen.get_size()
        if x != None:
            self.relativeX = x / self.W
            self.x = self.relativeX * screenW
        if y != None:
            self.relativeY = y / self.H
            self.y = self.relativeY * screenH

    def render(self):
        pg.draw.rect(self.screen, self.color, (self.x, self.y,  self.ObjectW, self.ObjectH))

class DynamicImage():
    def __init__(self, x, y, ObjectScale, image:pg.Surface, manager, rotate = 0):
        self.screen = pg.display.get_surface()
        self.manager = manager
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H

        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.rotate = rotate
        self.imageSave = image
        self.scale = ObjectScale / self.W
        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * screenW)

    def resize(self):
        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * screenW)

    def changeCoord(self, x, y):
        screenW, screenH = self.screen.get_size()
        if x != None:
            self.relativeX = x / self.W
            self.x = self.relativeX * screenW
        if y != None:
            self.relativeY = y / self.H
            self.y = self.relativeY * screenH

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
        self.relativeW = ObjectW / W
        self.relativeH = ObjectH / H

        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.element = pgu.elements.UITextEntryLine(
            relative_rect=pg.Rect((self.x, self.y), (ObjectW, ObjectH)),
            manager=self.manager,
            placeholder_text=defaultText
        )
    def resize(self):
        screenW, screenH = pg.display.get_surface().get_size()
        self.element.set_dimensions((self.relativeW * screenW, self.relativeH * screenH))
        self.element.set_position((self.relativeX * screenW, self.relativeY * screenH))

class DynamicButton():
    def __init__(self, x, y, ObjectW, ObjectH, text, manager, ids = ObjectID("","")):
        self.screen = pg.display.get_surface()
        self.manager = manager
        W = 1280
        H = 720
        self.relativeX = x / W
        self.relativeY = y / H
        self.relativeW = ObjectW / W
        self.relativeH = ObjectH / H
        screenW, screenH = pg.display.get_surface().get_size()
        
        self.element = pgu.elements.UIButton(
            relative_rect=pg.Rect((self.relativeX * screenW, self.relativeY * screenH), (self.relativeW * screenW, self.relativeH * screenH)),
            text=text,
            object_id=ids,
            manager=self.manager
        )

    def resize(self):
        screenW, screenH = pg.display.get_surface().get_size()
        self.element.set_relative_position((self.relativeX * screenW, self.relativeY * screenH))
        self.element.set_dimensions((self.relativeW * screenW, self.relativeH * screenH))