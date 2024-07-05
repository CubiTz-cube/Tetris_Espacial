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
        self.userData = ["","", "", gv.states[1], []]
        self.manager = pgu.UIManager((self.W,self.H), "pages\\css\\loginRegister.json")
        self.manager.get_theme().load_theme("pages\\css\\global.json")
        self.isLoad = False

        self.inputName = DynamicInput(740, 250, 460, 75, self.manager, "Nombre y apellido")
        self.inputPassword = DynamicInput(740, 330, 460, 75, self.manager, "Contraseña")
        self.inputMail = DynamicInput(740, 410, 220, 75, self.manager, "Correo")
        self.inputState = DynamicInput(980, 410, 220, 75, self.manager, "Estado", options=gv.states[1:])
        self.buttonPlay = DynamicButton(790, 510, 360, 70, "Iniciar", self.manager, ObjectID("#play"))
        self.buttonLogin = DynamicButton(790, 580, 360, 50, "¿Tienes cuenta? inicia sesion", self.manager, ObjectID("#register"))
        self.textError = DynamicText(640, 620, "",gv.fontLekton, 18, "#AD1106")

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
                self.userData[2] = self.inputName.element.get_text()

            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState.element:
                self.userData[3] = self.inputState.element.selected_option[0]
                self.userData[3] = self.inputState.element.selected_option[1]

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword.element:
                self.userData[1] = self.inputPassword.element.get_text()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail.element:
                self.userData[0] = self.inputMail.element.get_text()

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
                mail=self.userData[0]
                password=self.userData[1]
                name=self.userData[2]
                validacion=[self.validatePassword(password),self.validateEmail(mail)]
                print("------------------------------------RESULTADOS DE LA VALIDACION-----------------------------------")
                print(f"valores de validacion son: {validacion}")
                print(f"All validacion: {all(validacion)}, VALIDATE GLOBAL(MAIL):{self.validateGlobal(mail)} ,VALIDATE GLOBAL: PASSWORD:{self.validateGlobal(password)} ,VALIDATE GLOBAL NAME: {self.validateGlobal(name)}, NO DUPLICATE Mail: {self.No_duplicate_mail(mail)}")
                if all(validacion[0]) and all(validacion) and self.validateGlobal(mail) and self.validateGlobal(password) and self.validateGlobal(name) and self.No_duplicate_mail(mail):
                    self.saveUser()
                    gv.actualUser=self.userData
                    gv.actualPage = 2
                elif(self.validateGlobal(name)!=True):
                    print("validando nombre")
                    self.textError.changeText("*El nombre no debe contener | o estar vacio.")
                elif(validacion[0][0]!=True):
                    print("validando password 1:  ",validacion[0][0])
                    self.textError.changeText("*Contraseña no valida.\nTiene ñ, no tiene al menos una mayuscula y minuscula o\ntiene acentos o caracteres especiales\naparte de los permitidos (*=.-)")
                elif(validacion[0][1]!=True):
                        print("validando password 2:  ", validacion[0][1])
                        self.textError.changeText("*Contrasena no válida.\nNo tiene al menos uno de los caracteres (*=.-)")
                elif(validacion[0][2]!=True):
                            print('validando passowrd 3:  ',validacion[0][2])
                            self.textError.changeText("contrasena no válida\nSe repite 3 veces el mismo caracter")
                elif(validacion[1]!=True or self.validateGlobal(mail)!=True):
                    print(f"validacion del mail es:{self.validateEmail(mail)}")
                    print("validando mail")
                    self.textError.changeText("Correo no válido.\nDebe ser un correo de Gmail o Hotmail y no debe estar vacio.")
                elif(self.No_duplicate_mail(mail) !=True):
                    print("validando email duplicado")
                    self.textError.changeText("Correo no válido.\nEste correo ya esta registrado")
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLogin.element:
                gv.actualPage = 0
                self.isLoad = False
                

            self.manager.process_events(event)

    def validatePassword(self, str):
        valid = [True, True, True]
        # No tiene ñ, tiene almenos una mayuscula y minuscula no tiene acentos ni caracteres especiales aparte de los permitidos (*=.-)
        if bool(re.search(r'[ñÑ]', str)): valid[0] = False
        if not (bool(re.search(r'[a-z]', str)) and bool(re.search(r'[A-Z]', str))): valid[0] = False
        if bool(re.search(r'[áéíóúÁÉÍÓÚ]', str)): valid[0] = False
        if bool(re.search(r'[^\w=*-.]', str)): valid[0] = False

        # Tiene al menos uno de los caracteres (*=.-)
        if not bool(re.search(r'[=*-.]', str)): valid[1] = False

        # No se repite 3 veces el mismo caracter
        if bool(re.search(r'(.)\1\1', str)): valid[2] = False
        
        return valid
    
    def validateGlobal(self, text:str):
        if "@gmail.com" in text or "@hotmail.com" in text:
            if text.startswith("@gmail.com") or text.startswith("@hotmail.com"):
                return False
        if text=="" or "|" in text: 
            return False
        else:
            return True

    def validateEmail(self,email:str):
        if not (email.endswith("@gmail.com") or email.endswith("@hotmail.com")):
            return False

        return True

    def No_duplicate_mail(self,email:str):
        j=0
        usuarios=getAllUsers()
        while j<len(usuarios) and usuarios[j][0]!=None:
            if usuarios[j][0] == email:
                return False 
            else:
                j+=1
        return True
    
    def frontEnd(self):
        self.screen.fill("#050611")

        for obj in self.dynamicObjects:
            obj.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def backEnd(self):
        pass

    def saveUser(self):
        for i in self.userData:
            if i == "":
                return
        with open(gv.fileUsers, "ab") as file:
            for index, data in enumerate(self.userData):
                print("Writing data to file")

                text  = ""
                if index != len(self.userData)-1: text = str(data)+"|"
                else: text = str(data)

                file.write(text.encode())
            file.write(b"\n")
    
    def bucle(self):
        if not self.isLoad:
            self.resize()
            self.isLoad = True

        self.events()
        self.frontEnd()
        self.backEnd()
