import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID
import math

class DynamicText():
    def __init__(self, x:float, y:float, text:str, fontPath:str, size:int, color):
        self.screen = pg.display.get_surface()
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H
        self.relativeSize = size / self.W
        self.fontPath = fontPath
        self.text = text
        self.color = color

        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX  * screenW
        self.y = self.relativeY * screenH
        self.size = int(self.relativeSize * screenW)

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
    def __init__(self, x, y, ObjectW, ObjectH, color, border = 0, borderColor = "#000000"):
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
        self.border = border
        self.borderColor = borderColor

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
        if self.border != 0:
            pg.draw.rect(self.screen, self.borderColor, (self.x-self.border, self.y-self.border,  self.ObjectW+self.border*2, self.ObjectH+self.border*2), self.border)

class DynamicImage():
    def __init__(self, x, y, ObjectScale, image:pg.Surface, rotate = 0, mirror = False):
        self.screen = pg.display.get_surface()
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H

        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.rotate = rotate
        self.imageSave = image
        self.mirror = mirror
        self.scale = ObjectScale / self.W
        self.alfa = 255

        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * screenW)
        if self.mirror:
            self.image = pg.transform.flip(self.image, True, False)
        self.image.set_alpha(self.alfa)

    def resize(self):
        screenW, screenH = self.screen.get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.image = pg.transform.rotozoom(self.imageSave, self.rotate, self.scale * screenW)
        if self.mirror:
            self.image = pg.transform.flip(self.image, True, False)

    def changeCoord(self, x, y):
        screenW, screenH = self.screen.get_size()
        if x != None:
            self.relativeX = x / self.W
            self.x = self.relativeX * screenW
        if y != None:
            self.relativeY = y / self.H
            self.y = self.relativeY * screenH

    def changeImg(self, image:pg.Surface):
        self.imageSave = image
        self.resize()

    def changeAlfa(self, alfa):
        self.alfa = alfa
        self.image.set_alpha(self.alfa)

    def render(self):
        self.screen.blit(self.image, (self.x, self.y))

class DynamicInput():
    def __init__(self, x, y, ObjectW, ObjectH, manager, defaultText="", options = []):
        self.screen = pg.display.get_surface()
        self.manager = manager
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H
        self.relativeW = ObjectW / self.W
        self.relativeH = ObjectH / self.H
        

        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.ObjectW = self.relativeW * screenW
        self.ObjectH = self.relativeH * screenH
        if options:
            self.element = pgu.elements.UIDropDownMenu(
                options_list=options,
                starting_option=options[0] if options else defaultText,
                relative_rect=pg.Rect((self.x, self.y), (self.ObjectW, self.ObjectH)),
                manager=self.manager
            )
        else:
            self.element = pgu.elements.UITextEntryLine(
                relative_rect=pg.Rect((self.x, self.y), (self.ObjectW, self.ObjectH)),
                manager=self.manager,
                placeholder_text=defaultText
            )
    def resize(self):
        screenW, screenH = pg.display.get_surface().get_size()
        self.element.set_dimensions((self.relativeW * screenW, self.relativeH * screenH))
        self.element.set_position((self.relativeX * screenW, self.relativeY * screenH))

    def render(self):
        pass
        
class DynamicDropDown():
    def __init__(self, x, y, ObjectW, ObjectH, manager, options = [], defaultText=None):
        self.screen = pg.display.get_surface()
        self.manager = manager
        self.W = 1280
        self.H = 720
        self.relativeX = x / self.W
        self.relativeY = y / self.H
        self.relativeW = ObjectW / self.W
        self.relativeH = ObjectH / self.H
        

        screenW, screenH = pg.display.get_surface().get_size()
        self.x = self.relativeX * screenW
        self.y = self.relativeY * screenH
        self.ObjectW = self.relativeW * screenW
        self.ObjectH = self.relativeH * screenH

        self.element = pgu.elements.UIDropDownMenu(
            options_list=options,
            starting_option=defaultText if defaultText else options[0],
            relative_rect=pg.Rect((self.x, self.y), (self.ObjectW, self.ObjectH)),
            manager=self.manager
        )

    def resize(self):
        screenW, screenH = pg.display.get_surface().get_size()
        self.element.set_dimensions((self.relativeW * screenW, self.relativeH * screenH))
        self.element.set_position((self.relativeX * screenW, self.relativeY * screenH))

    def render(self):
        pass

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

    def render(self):
        pass