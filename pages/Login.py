import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

from library.dataFormating import getAllUsers
import public.images.loadImages as img

class DynamicText():
    def __init__(self, text, x, y, fontPath, size, color):
        self.screen = pg.display.get_surface()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.relativeX = x / W
        self.relativeY = y / H
        self.relativeSize = size / W
        self.x = x
        self.y = y
        self.text = text
        self.font:pg.Font = pg.font.Font(fontPath, size)
        self.fontPath = fontPath
        self.color = color

    def resize(self, W:int, H:int):
        self.x = self.relativeX * W
        self.y = self.relativeY * H
        self.font = pg.font.Font(self.fontPath, int(self.relativeSize * W))

    def render(self):
        self.screen.blit(self.font.render(self.text, True, self.color), (self.x, self.y))

class DynamicInput():
    def __init__(self, x, y, ObjectW, ObjectH, manager):
        self.screen = pg.display.get_surface()
        self.manager = manager
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.relativeX = x / W
        self.relativeY = y / H
        self.x = x
        self.y = y
        self.relativeW = ObjectW / W
        self.relativeH = ObjectH / H
        self.input = pgu.elements.UITextEntryLine(
            relative_rect=pg.Rect((self.x, self.y), (ObjectW, ObjectH)),
            manager=self.manager
        )
    def resize(self, W, H):
        self.input.set_dimensions((self.relativeW * W, self.relativeH * H))
        self.input.set_position((self.relativeX * W, self.relativeY * H))
    def render(self):
        pass

class Login():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((W,H), "pages\\css\\loginRegister.json")
        self.manager.get_theme().load_theme("pages\\css\\global.json")

        self.user = ["", ""]
        self.allUsers = getAllUsers(gv.fileUsers)

        for user in self.allUsers:
            print(user)

        self.renderTextData = [pg.font.Font(None, 32).render(str(inpu), True, (255,255,255)) for inpu in self.user]  
        self.renderTextInvalid = [
            pg.font.Font(None, 32).render("", True, (255,255,255)),
            pg.font.Font(None, 32).render("Correo no encontrado", True, (255,255,255)),
            pg.font.Font(None, 32).render("Password incorrect", True, (255,255,255)),
        ] 
        self.invalidText = 0

        #pg.Rect(((W/2 - W/2.5)/2, W/8), (W/2.5, W/12))
        """self.textTitle = pgu.elements.UILabel(
            relative_rect=pg.Rect(((W/2 - W/2.5)/2, H/6), (W/2.5, W/12)),
            text="¡Bienvenido!",
            object_id= ObjectID("","@title"),
            manager=self.manager,
        )"""

        self.textList = [
            DynamicText("¡Bienvenido!", (W/2 - pg.font.Font(gv.fontAldrich, 100).size("¡Bienvenido!")[0])/2, H/6, gv.fontAldrich, 100, "#000000"),
            DynamicText("Tetris", W - pg.font.Font(gv.fontAldrich, 80).size("Tetris")[0]*1.1, H - pg.font.Font(gv.fontAldrich, 80).size("Tetris")[1], gv.fontAldrich, 80, "#FFFFFF"),        
        ]
        self.inputMail = DynamicInput(250, 50, 500, 30, self.manager)
        
        self.inputPassword = DynamicInput(250, 100, 500, 30, self.manager)

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 250), (100, 50)),
        text="Play",
        manager=self.manager)

        self.buttonRegister = pgu.elements.UIButton(
        relative_rect=pg.Rect((450, 250), (100, 50)),
        text="Register",
        manager=self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                print("resize")
                self.resizeUI()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail.input:
                self.user[0] = self.inputMail.input.get_text()
                self.renderTextData[0] = pg.font.Font(None, 32).render(self.user[0], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword.input:
                self.user[1] = self.inputPassword.input.get_text()
                self.renderTextData[1] = pg.font.Font(None, 32).render(self.user[1], True, (255,255,255))

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonRegister:
                gv.actualPage = 1

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                result = self.searchUser()
                if all(result):
                    gv.actualPage = 2
                elif result[0] and not result[1]:
                    self.invalidText = 2
                else:
                    self.invalidText = 1

            self.manager.process_events(event)

    def resizeUI(self):
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h

        self.inputMail.resize(W, H)
        
        for text in self.textList:
            text.resize(W, H)

    def searchUser(self):
        userFind = False
        passwordFind = False

        for outer in self.allUsers:
            if (outer[0] == self.user[0]):
                userFind = True
                if (outer[1] == self.user[1]):
                    passwordFind = True
                    gv.actualUser = outer

        return [userFind, passwordFind]

    def drawBackground(self):
        self.screen.fill("#050611")
        pg.draw.rect(self.screen, "#FFFFFF", (0, 0, pg.display.Info().current_w/2, pg.display.Info().current_h))


    def frontEnd(self):
        self.drawBackground()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderTextData):
            self.screen.blit(text, (0, 50*index))

        self.screen.blit(self.renderTextInvalid[self.invalidText], (0, 150))
        for text in self.textList:
            text.render()
    
    def bucle(self):
        self.events()
        self.frontEnd()