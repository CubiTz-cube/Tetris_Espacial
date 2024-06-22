import pygame as pg
import pygame_gui as pgu
from library.encrypter import encrypt, decrypt
from library.dataFormating import getAllUsers 
import globalVariables as gv
import re


class Register():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))
        self.userData = ["correo","password", "name", "state"]
        gv.font = pg.font.Font(gv.fontLekton, 32)
        self.renderText = [gv.font.render(str(data), True, (255,255,255)) for data in self.userData]
        self.inputName = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 0), (500, 30)),
        manager=self.manager)

        self.inputState = pgu.elements.UIDropDownMenu(
        relative_rect=pg.Rect((250, 100), (500, 30)),
        starting_option="Bolívar",
        options_list=gv.states[1:],
        manager=self.manager)

        self.inputPassword = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 150), (500, 30)),
        manager=self.manager)

        self.inputMail = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 200), (500, 30)),
        manager=self.manager)

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 250), (100, 50)),
        text="Play",
        manager=self.manager)

        self.buttonLogin = pgu.elements.UIButton(
        relative_rect=pg.Rect((450, 250), (100, 50)),
        text="Login",
        manager=self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_element == self.inputName:
                self.userData[1] = self.inputMail.get_text()
                print("Dropping down menu",self.userData[1])
                self.renderText[1] = self.font.render(self.userData[1], True, (255,255,255))

            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState:
                print("Dropping down menu",self.userData[3])
                self.userData[3] = self.inputState.selected_option[1]
                self.renderText[3] = gv.font.render(self.userData[3], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_element == self.inputPassword:
                self.userData[4] = self.inputPassword.get_text()
                print("Dropping down menu",self.userData[4])
                self.renderText[4] = gv.font.render(self.userData[4], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_element == self.inputMail:
                print("Dropping down menu",self.userData[5])
                self.userData[5] = self.inputMail.get_text()
                self.renderText[5] = gv.font.render(self.userData[5], True, (255,255,255))

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                self.saveUser()
                gv.actualPage = 2
            
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLogin:
                gv.actualPage = 0

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
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderText[1:-1]):
            self.screen.blit(text, (0, 50*index))

    def backEnd(self):
        pass

    def saveUser(self):
        with open(gv.fileUsers, "ab") as file:
            for data in self.userData:
                print("Writing data to file")
                file.write((encrypt(str(data))+" ").encode())
            file.write(b"\n")
    
    def bucle(self):
        self.events()
        self.frontEnd()
        self.backEnd()
