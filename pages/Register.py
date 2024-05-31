import pygame as pg
import pygame_gui as pgu
from library.encrypter import encrypt, decrypt

import globalVariables as gv

class Register():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))
        self.font = pg.font.Font(None, 32)
        self.mouseUP = False

        self.userData = ["code","name", "lastName", "state", "password", "mail", []]
        self.renderText = [self.font.render(str(data), True, (255,255,255)) for data in self.userData]

        self.inputName = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 0), (500, 30)),
        manager=self.manager,
        object_id="#inputName")

        self.inputLastName = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 50), (500, 30)),
        manager=self.manager,
        object_id="#inputLastName")

        self.inputState = pgu.elements.UIDropDownMenu(
        relative_rect=pg.Rect((250, 100), (500, 30)),
        starting_option="Bolivar",
        options_list=["Bolivar", "Anzoategui", "Carabobo"],
        manager=self.manager,
        object_id="#inputState")

        self.inputPassword = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 150), (500, 30)),
        manager=self.manager,
        object_id="#inputPassword")

        self.inputMail = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 200), (500, 30)),
        manager=self.manager,
        object_id="#inputMail")

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 250), (100, 50)),
        text="Play",
        manager=self.manager,
        object_id="#buttonPlay")

        self.buttonLogin = pgu.elements.UIButton(
        relative_rect=pg.Rect((450, 250), (100, 50)),
        text="Login",
        manager=self.manager,
        object_id="#buttonLogin")

    def validate_password(self, password):
        special_chars = '*-=.'
        valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890*-=.'
            
        rule_1 = 8 <= len(password) <= 10
        for i in password:
            if i not in valid_chars or i in 'Ññ':
                rule_1 = False
                break

        rule_2 = False
        for i in password:
            if i in special_chars:
                rule_2 = True
                break

        rule_3 = True
        for i in password:
            if i not in valid_chars:
                rule_3 = False
                break

        rule_4 = True
        for i in range(len(password) - 3):
            if password[i] == password[i+1] == password[i+2] == password[i+3]:
                rule_4 = False
                break

        return [rule_1, rule_2, rule_3, rule_4]

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pg.MOUSEBUTTONUP:
                self.mouseUP = True
            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputName":
                self.userData[1] = self.inputName.get_text()
                self.renderText[1] = self.font.render(self.userData[1], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputLastName":
                self.userData[2] = self.inputLastName.get_text()
                self.renderText[2] = self.font.render(self.userData[2], True, (255,255,255))

            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "#inputState":
                self.userData[3] = self.inputState.selected_option[0]
                self.renderText[3] = self.font.render(self.userData[3], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputPassword":
                self.userData[4] = self.inputPassword.get_text()
                self.renderText[4] = self.font.render(self.userData[4], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputMail":
                self.userData[5] = self.inputMail.get_text()
                self.renderText[5] = self.font.render(self.userData[5], True, (255,255,255))

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonPlay":
                code = self.codeGenerator()
                self.saveBinary(code)
                gv.actualPage = 2
            
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonLogin":
                gv.actualPage = 0

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderText[1:-1]):
            self.screen.blit(text, (0, 50*index))

    def backEnd(self):
        pass

    #FUNCION RECURSIVA CALCULAR CODIGO UNICO
    def calculate_code(data, index=0):
        if not data:
            return 0
        else:
            value = data[0]
            code = len(value) * index
            return code + calculate_code(data[1:], index + 1)

        code = calculate_code(self.userData)
        self.userData[0] = str(code)
    
    def saveBinary(self, code:int):
        with open("./data/JUGADORES.bin", "rb") as file:
                preInfo:list[bin] = file.readlines()

        with open("./data/JUGADORES.bin", "wb") as file:
            file.writelines(preInfo)
            for data in self.userData:
                file.write((encrypt(str(data))+" ").encode())
            file.write(b"\n")
    
    def bucle(self):
        self.events()
        self.frontEnd()
        self.backEnd()