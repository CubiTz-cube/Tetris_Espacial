import pygame as pg
import pygame_gui as pgu
from library.encrypter import encrypt, decrypt
from library.dataFormating import getAllUsers 
import globalVariables as gv
from library.dynamicObjects import *
import public.images.loadImages as img
import re
from pygame_gui.core import ObjectID


class Register():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))
        self.userData = ["correo","password", "name", "state"]
        self.manager = pgu.UIManager((self.W,self.H), "pages\\css\\loginRegister.json")
        self.manager.get_theme().load_theme("pages\\css\\global.json")
        self.isLoad = False

        self.inputName = DynamicInput(740, 250, 460, 75, gv.fontAldrich, 24, "#000000", self.manager, "Nombre y apellido")
        self.inputPassword = DynamicInput(740, 330, 460, 75, gv.fontAldrich, 24, "#000000", self.manager, "Contraseña")
        self.inputMail = DynamicInput(740, 410, 220, 75, gv.fontAldrich, 24, "#000000", self.manager, "Correo")
        self.inputState = DynamicInput(980, 410, 220, 75, gv.fontAldrich, 24, "#000000", self.manager, "Estado", options=gv.states[1:])
        self.buttonPlay = DynamicButton(790, 510, 360, 70, "Iniciar", self.manager, ObjectID("#play"))
        self.buttonLogin = DynamicButton(790, 580, 360, 50, "¿Tienes cuenta? inicia sesion", self.manager, ObjectID("#register"))
        self.textError = DynamicText(640, 460, "",gv.fontLekton, 26, "#AD1106")

        self.dynamicObjects = [
            self.inputName,
            self.inputPassword,
            self.inputMail,
            self.inputState,
            self.buttonPlay,
            self.buttonLogin,
            DynamicRect(640, 0, 640, 720, "#FFFFFF"),
            DynamicImage(650, 10, 0.085, img.logos["isotipoNegro"]),
            DynamicText((1988 - pg.font.Font(gv.fontAldrich, 85).size("Registrate  ")[0])/2, 120,"Registrate", gv.fontAldrich, 85, "#000000"),
            DynamicText(210 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[0], 720 - pg.font.Font(gv.fontAldrich, 65).size("Tetris")[1],"Tetris", gv.fontAldrich, 65, "#ffffff"),
            self.textError,
            DynamicImage(460, 30, 0.65, img.completePieces["red"], rotate = -15, mirror=True),
            DynamicImage(210, 0, 0.65, img.completePieces["purple"], rotate = 5, mirror=True),
            DynamicImage(-80, 100, 0.65, img.completePieces["blueBlack"], rotate = -78, mirror=True),
            DynamicImage(270, 200, 0.65, img.completePieces["orange"], rotate = -5, mirror=True),
            DynamicImage(370, 350, 0.65, img.completePieces["green"], rotate = -16, mirror=True),
            DynamicImage(10, 350, 0.65, img.completePieces["blue"], rotate = -15, mirror=True),
            DynamicImage(215, 530, 0.65, img.completePieces["yellow"], rotate = 23, mirror=True),
            DynamicImage(500, 600, 0.65, img.completePieces["greenBlue"], rotate = -24, mirror=True),
        ]

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resize()
                pass
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputName.element:
                self.userData[2] = self.inputName.element.get_text() #le coloco element porque ya le puse element a lo demas tomces mi logica me dice que esto tambien
                print("Dropping down menu",self.userData)

            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState.element:
                print("Dropping down menu",self.userData)
                self.userData[3] = self.inputState.element.selected_option[0]
                self.userData[3] = self.inputState.element.selected_option[1]

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword.element:
                self.userData[1] = self.inputPassword.element.get_text()
                print("Dropping down menu",self.userData)

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail.element:
                print("Dropping down menu",self.userData)
                self.userData[0] = self.inputMail.element.get_text()

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
                self.saveUser()
                gv.actualPage = 2
            
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLogin.element:
                gv.actualPage = 0
                self.isLoad = False

            self.manager.process_events(event)

    def validatePassword(str):
        valid = [True, True, True]
        # No tiene ñ, tiene almenos una mayuscula y minuscula no tiene acentos ni caracteres especiales aparte de los permitidos (*=.-)
        if bool(re.search(r'[ñÑ]', str)): valid[0] = False
        if not (bool(re.search(r'[a-z]', str)) and bool(re.search(r'[A-Z]', str))): valid[0] = False
        if bool(re.search(r'[áéíóúÁÉÍÓÚ]', str)): valid[0] = False
        if bool(re.search(r'[^\w=*-.]', str)): valid[0] = False

        # Tiene al menos uno de los caracteres (*=.-)
        if not bool(re.search(r'[=*-.]', str)): valid[1] = False

        # No se repite 3 veces el mismo caracter
        if bool(re.search(r'(.)\1\1\1', str)): valid[2] = False

        return valid
    
    def validate_email(email):
        valid = False

        if "@" in email:
            valid = True

        if valid[0] and ".com" in email.split("@")[1]:
            valid = True

        if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$", email):
            valid = True

        if not (email.startswith(".") or email.endswith(".") or email.startswith("@") or email.endswith("@")):
            valid = True

        if ".." not in email and "@@" not in email and ".@" not in email and "@." not in email:
            valid = True

        if email.endswith(".com") and email.count(".com") == 1:
            valid = True

        return valid
    
    def frontEnd(self):
        self.screen.fill("#050611")

        for obj in self.dynamicObjects:
            obj.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def backEnd(self):
        pass

    def saveUser(self):
        with open(gv.fileUsers, "ab") as file:
            for data in self.userData:
                print("Writing data to file")
                file.write((encrypt(str(data))+" ").encode())
            file.write(b"\n")
    
    def bucle(self):
        if not self.isLoad:
            self.resize()
            self.isLoad = True

        self.events()
        self.frontEnd()
        self.backEnd()
