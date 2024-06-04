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

        self.user = ["", ""]
        self.allUsers = []
        with open("./data/JUGADORES.bin", "rb") as file:
            lines = file.readlines()
            for line in lines:
                self.allUsers.append(line.decode().replace("\n", "").split(" "))

        print(self.allUsers)

        self.userInputs = ["mail","password"]
        self.renderTextData = [pg.font.Font(None, 32).render(str(inpu), True, (255,255,255)) for inpu in self.userInputs]  
        self.renderTextInvalid = [
            pg.font.Font(None, 32).render("", True, (255,255,255)),
            pg.font.Font(None, 32).render("Correo no encontrado", True, (255,255,255)),
            pg.font.Font(None, 32).render("Password incorrect", True, (255,255,255)),
        ] 
        self.invalidText = 0

        self.userInputsUI = []
        for index, inpu in enumerate(self.userInputs):
            self.userInputsUI.append(
                pgu.elements.UITextEntryLine(
                    relative_rect=pg.Rect((250, 50*index), (500, 30)),
                    manager=self.manager
                )
            )

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
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.userInputsUI[0]:
                self.user[0] = self.userInputsUI[0].get_text()
                self.renderTextData[0] = pg.font.Font(None, 32).render(self.user[0], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.userInputsUI[1]:
                self.user[1] = self.userInputsUI[1].get_text()
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

    def searchUser(self):
        userFind = False
        passwordFind = False

        for outer in self.allUsers:
            if (outer[0] == self.user[0]):
                userFind = True
                if (outer[1] == self.user[1]):
                    passwordFind = True

        return [userFind, passwordFind]

    def frontEnd(self):
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderTextData):
            self.screen.blit(text, (0, 50*index))

        self.screen.blit(self.renderTextInvalid[self.invalidText], (0, 150))
    
    def bucle(self):
        self.events()
        self.frontEnd()