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
        self.allUsers = getAllUsers()

        for user in self.allUsers:
            print(user)

        self.inputMail = DynamicInput(100, 250, 460, 85, gv.fontAldrich, 24, "#000000", self.manager, "Correo")
        self.inputPassword = DynamicInput(100, 360, 460, 85, gv.fontAldrich, 24, "#000000", self.manager, "Contraseña")

        self.buttonPlay = DynamicButton(150, 510, 360, 70, "Iniciar", self.manager, ObjectID("#play"))
        self.buttonRegister = DynamicButton(150, 580, 360, 50, "¿No tienes cuenta? Registrate", self.manager, ObjectID("#register"))

        self.textError = DynamicText(640, 460, "",gv.fontLekton, 26, "#AD1106")

        self.dynamicObjects = [
            DynamicRect(0, 0, 640, 720, "#FFFFFF"),
            DynamicImage(10, 10, 0.085, img.logos["isotipoNegro"], self.manager),
            DynamicText((640 - pg.font.Font(gv.fontAldrich, 85).size("¡Bienvenido!")[0])/2, 120,"¡Bienvenido!", gv.fontAldrich, 85, "#000000"),
            DynamicText(1260 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[0], 720 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[1],"Tetris", gv.fontAldrich, 65, "#FFFFFF"), 
            self.textError,
            DynamicImage(700, 30, 0.65, img.completePieces["red"], self.manager, rotate = -15),
            DynamicImage(950, 0, 0.65, img.completePieces["purple"], self.manager, rotate = 5),
            DynamicImage(1190, 100, 0.65, img.completePieces["blueBlack"], self.manager, rotate = -78),
            DynamicImage(915, 200, 0.65, img.completePieces["orange"], self.manager, rotate = -5),
            DynamicImage(775, 350, 0.65, img.completePieces["green"], self.manager, rotate = -16),
            DynamicImage(1125, 350, 0.65, img.completePieces["blue"], self.manager, rotate = -15),
            DynamicImage(980, 530, 0.65, img.completePieces["yellow"], self.manager, rotate = 23),
            DynamicImage(650, 600, 0.65, img.completePieces["greenBlue"], self.manager, rotate = -24),
        ]

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

            if (event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element )or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                result = self.searchUser()
                if all(result):
                    gv.actualPage = 2
                elif result[0] and not result[1]:
                    self.invalidText = 2
                    self.textError.changeText("*Contraseña incorrecta")
                    self.textError.changeCoord((640 - pg.font.Font(gv.fontLekton, 26).size("*Contraseña incorrecta")[0])/2, None)
                else:
                    self.invalidText = 1
                    self.textError.changeText("*Correo no encontrado")
                    self.textError.changeCoord((640 - pg.font.Font(gv.fontLekton, 26).size("*Correo no encontrado")[0])/2, None)

            self.manager.process_events(event)

    def resizeUI(self):
        self.inputMail.resize()
        self.inputPassword.resize()

        self.buttonPlay.resize()
        self.buttonRegister.resize()
        
        for text in self.dynamicObjects:
            text.resize()

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

    def changeRegisterAnimation(self):
        self.inputMail.element.visible = False
        self.inputPassword.element.visible = False
        self.buttonPlay.element.visible = False
        self.buttonRegister.element.visible = False

        self.dynamicObjects[0].changeCoord(640, None)
        self.dynamicObjects[1].changeCoord(1180, None)
        self.dynamicObjects[2].changeText("")
        self.dynamicObjects[3].changeCoord(20, None)
        self.dynamicObjects[5].changeCoord(480, None)

    def resetScreen(self):
        self.inputMail.element.visible = True
        self.inputPassword.element.visible = True
        self.buttonPlay.element.visible = True
        self.buttonRegister.element.visible = True

        self.dynamicObjects[0].changeCoord(0, None)
        self.dynamicObjects[1].changeCoord(10, None)
        self.dynamicObjects[2].changeText("¡Bienvenido!")
        self.dynamicObjects[3].changeCoord((640 - pg.font.Font(gv.fontAldrich, 85).size("¡Bienvenido!")[0])/2, None)
        self.dynamicObjects[5].changeCoord(10, None)

    def frontEnd(self):
        self.screen.fill("#050611")

        for text in self.dynamicObjects:
            text.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)
    
    def bucle(self):
        self.frontEnd()
        self.events()