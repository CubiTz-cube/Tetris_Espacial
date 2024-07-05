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
        self.isLoad = False

        self.user = ["", ""]
        self.allUsers = getAllUsers()

        gv.actualUser = self.allUsers[0]

        self.inputMail = DynamicInput(100, 250, 460, 85, self.manager, "Correo")
        self.inputPassword = DynamicInput(100, 340, 460, 85, self.manager, "Contraseña")

        self.buttonPlay = DynamicButton(150, 510, 360, 70, "Iniciar", self.manager, ObjectID("#play"))
        self.buttonRegister = DynamicButton(150, 580, 360, 50, "¿No tienes cuenta? Registrate", self.manager, ObjectID("#register"))

        self.textError = DynamicText(640, 460, "",gv.fontLekton, 26, "#AD1106")

        self.background = DynamicRect(0, 0, 640, 720, "#FFFFFF")
        self.imgLogo = DynamicImage(10, 10, 0.085, img.logos["isotipoNegro"])
        self.textWelcome = DynamicText((640 - pg.font.Font(gv.fontAldrich, 85).size("¡Bienvenido!")[0])/2, 120,"¡Bienvenido!", gv.fontAldrich, 85, "#000000")
        self.textTetris = DynamicText(1260 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[0], 720 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[1],"Tetris", gv.fontAldrich, 65, "#FFFFFF")
        self.imgRed = DynamicImage(700, 30, 0.65, img.completePieces["red"], rotate = -15)
        self.imgPurple = DynamicImage(950, 0, 0.65, img.completePieces["purple"], rotate = 5)
        self.imgBlueBlack = DynamicImage(1190, 100, 0.65, img.completePieces["blueBlack"], rotate = -78)
        self.imgOrange = DynamicImage(915, 200, 0.65, img.completePieces["orange"], rotate = -5)
        self.imgGreen = DynamicImage(775, 350, 0.65, img.completePieces["green"], rotate = -16)
        self.imgBlue = DynamicImage(1125, 350, 0.65, img.completePieces["blue"], rotate = -15)
        self.imgYellow = DynamicImage(980, 530, 0.65, img.completePieces["yellow"], rotate = 23)
        self.imgGreenBlue = DynamicImage(650, 600, 0.65, img.completePieces["greenBlue"], rotate = -24)
        self.dynamicObjects = [
            self.background,
            self.imgLogo,
            self.textWelcome,
            self.textTetris,
            self.imgRed,
            self.imgPurple,
            self.imgBlueBlack,
            self.imgOrange,
            self.imgGreen,
            self.imgBlue,
            self.imgYellow,
            self.imgGreenBlue,
            self.textError
        ]

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resize()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail.element:
                self.user[0] = self.inputMail.element.get_text()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword.element:
                self.user[1] = self.inputPassword.element.get_text()

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonRegister.element:
                gv.actualPage = 1
                self.isLoad = False

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

    def resize(self):
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
                    print(gv.actualUser)

        return [userFind, passwordFind]

    def frontEnd(self):
        self.screen.fill("#050611")

        for text in self.dynamicObjects:
            text.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)
    
    def bucle(self):
        if not self.isLoad:
            self.resize()
            self.isLoad = True

        self.frontEnd()
        self.events()