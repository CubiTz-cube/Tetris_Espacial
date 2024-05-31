import pygame as pg
import pygame_gui as pgu

import globalVariables as gv

class Login():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))
        self.mouseUP = False

        self.usersData = []
        with open("./data/JUGADORES.bin", "rb") as file:
            lines = file.readlines()
            for line in lines:
                self.usersData.append(line.decode().replace("\n", "").split(" "))


        self.userData = ["mail","password"]
        self.renderTextData = [pg.font.Font(None, 32).render(str(data), True, (255,255,255)) for data in self.userData]  
        self.renderTextInvalid = [
            pg.font.Font(None, 32).render("User not found", True, (255,255,255)),
            pg.font.Font(None, 32).render("Password incorrect", True, (255,255,255)),
            pg.font.Font(None, 32).render("", True, (255,255,255))
        ] 
        self.invalid = 2

        self.inputName = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 0), (500, 30)),
        manager=self.manager)

        self.inputPassword = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 150), (500, 30)),
        manager=self.manager)

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
                #Reside screen
                pass
            if event.type == pg.MOUSEBUTTONUP:
                self.mouseUP = True
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputName:
                self.userData[0] = self.inputName.get_text()
                self.renderTextData[0] = pg.font.Font(None, 32).render(self.userData[0], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword:
                self.userData[1] = self.inputPassword.get_text()
                self.renderTextData[1] = pg.font.Font(None, 32).render(self.userData[1], True, (255,255,255))

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonRegister:
                gv.actualPage = 1

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                check = self.checkUser()
                if check == 2:
                    gv.actualPage = 2
                else:
                    self.invalid = check

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderTextData):
            self.screen.blit(text, (0, 50*index))

        self.screen.blit(self.renderTextInvalid[self.invalid], (0,100))

    def checkUser(self):
        if len(self.usersData) == 0: return 0
        for user in self.usersData:
            print(user[1], user[5], user[4])
            print(self.userData[0], self.userData[1])
            if (self.userData[0] == user[1] or self.userData[1] == user[5]) and self.userData[1] == user[4]:
                return 2
            else:
                if self.userData[0] != user[1] and self.userData[1] != user[5]:
                    return 0
                elif self.userData[1] != user[4]:
                    return 1

    def saveBinary(self, code:int):
        with open("./data/JUGADORES.bin", "rb") as file:
                preInfo:list[bin] = file.readlines()

        with open("./data/JUGADORES.bin", "wb") as file:
            file.writelines(preInfo)
            for data in self.userData:
                file.write((str(data)+" ").encode())
            file.write(b"\n")
    
    def bucle(self):
        self.events()
        self.frontEnd()