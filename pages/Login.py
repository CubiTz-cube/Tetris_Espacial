import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

from library.dataFormating import getAllUsers
import public.images.loadImages as img
from library.dynamicObjects import *

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

        self.DynamicObjects = [
            DynamicImage(10, 10, 0.085, img.logos["isotipoNegro"], self.manager),
            DynamicImage(700, 30, 0.65, img.completePieces["red"], self.manager, rotate = -15),
            DynamicImage(950, 0, 0.65, img.completePieces["purple"], self.manager, rotate = 5),
            DynamicImage(1190, 100, 0.65, img.completePieces["pink"], self.manager, rotate = -78),
            DynamicImage(915, 200, 0.65, img.completePieces["orange"], self.manager, rotate = -5),
            DynamicImage(775, 350, 0.65, img.completePieces["green"], self.manager, rotate = -16),
            DynamicImage(1125, 350, 0.65, img.completePieces["blue"], self.manager, rotate = -15),
            DynamicImage(980, 530, 0.65, img.completePieces["yellow"], self.manager, rotate = 23),
            DynamicImage(650, 600, 0.65, img.completePieces["greenBlue"], self.manager, rotate = -24),
            DynamicText("¡Bienvenido!", (W/2 - pg.font.Font(gv.fontAldrich, 85).size("¡Bienvenido!")[0])/2, H/6, gv.fontAldrich, 85, "#000000"),
            DynamicText("Tetris", W - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[0]*1.1, H - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[1], gv.fontAldrich, 65, "#FFFFFF"),          
        ]
        self.inputMail = DynamicInput(100, 250, 460, 85, gv.fontAldrich, 24, "#000000", self.manager, "Correo")
        self.inputPassword = DynamicInput(100, 360, 460, 85, gv.fontAldrich, 24, "#000000", self.manager, "Contraseña")

        self.buttonPlay = DynamicButton(150, 510, 360, 65, "Iniciar", self.manager, ObjectID("#play"))
        self.buttonRegister = DynamicButton(150, 580, 360, 50, "¿No tienes cuenta? Registrate", self.manager, ObjectID("#register"))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resizeUI()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail.element:
                self.user[0] = self.inputMail.element.get_text()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword.element:
                self.user[1] = self.inputPassword.element.get_text()

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonRegister.element:
                gv.actualPage = 1

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
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
        self.inputPassword.resize(W, H)

        self.buttonPlay.resize(W, H)
        self.buttonRegister.resize(W, H)
        
        for text in self.DynamicObjects:
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
        for text in self.DynamicObjects:
            text.render()
    
    def bucle(self):
        self.events()
        self.frontEnd()