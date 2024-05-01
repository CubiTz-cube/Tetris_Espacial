import pygame as pg
import pygame_gui as pgu

class Register():
    def __init__(self, changePage) -> None:
        self.changePage = changePage
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
                self.changePage(2)
            
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonLogin":
                self.changePage(0)

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.renderText[1:-1]):
            self.screen.blit(text, (0, 50*index))

    def backEnd(self):
        pass

    def codeGenerator(self):
        #hacerlo de forma recursiva
        code = 0
        for index, value in enumerate(self.userData):
            code += len(value)*index
        
        self.userData[0] = str(code)
    
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
        self.backEnd()