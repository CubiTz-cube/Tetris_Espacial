import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

from library.dataFormating import getAllUsers
import public.images.loadImages as img

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

        self.textTitle = pgu.elements.UILabel(
            relative_rect=pg.Rect(((W/2 - W/2.5)/2, 0), (W/2.5, 140)),
            text="¡Bienvenido!",
            object_id= ObjectID("#textWelcome","@title"),
            manager=self.manager
        )

        self.textError = pgu.elements.UILabel(
            relative_rect=pg.Rect((W//2, 150), (100, 30)),
            text="Aqui errores",
            object_id=ObjectID("","@content"),
            manager=self.manager
        )

        self.inputMail = pgu.elements.UITextEntryLine(
            relative_rect=pg.Rect((250, 50), (500, 30)),
            manager=self.manager
        )
        self.inputPassword = pgu.elements.UITextEntryLine(
            relative_rect=pg.Rect((250, 100), (500, 30)),
            manager=self.manager
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
                print("resize")
                self.resizeUI()

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputMail:
                self.user[0] = self.inputMail.get_text()
                self.renderTextData[0] = pg.font.Font(None, 32).render(self.user[0], True, (255,255,255))

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputPassword:
                self.user[1] = self.inputPassword.get_text()
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
        self.textTitle.set_relative_position(((W/2 - W/2.5)/2, 0))
        self.textTitle.set_dimensions((W/2.5, 140))
        
        self.textError.set_relative_position((W//2, 150))

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