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

        self.userData:dict[str:str] = {
            "name": "nombre",
            "lastName": "Apellido",
            "state": "Bolivar",
            "password": "password",
            "mail": "hola@gmail.com",
        }

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

        self.render = [self.font.render(self.userData["name"], True, (255, 255, 255)), self.font.render(self.userData["lastName"], True, (255, 255, 255)), self.font.render(self.userData["state"], True, (255, 255, 255)), self.font.render(self.userData["password"], True, (255, 255, 255)), self.font.render(self.userData["mail"], True, (255, 255, 255))]

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
                self.userData["name"] = self.inputName.get_text()
                self.render[0] = self.font.render(self.userData["name"], True, (255, 255, 255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputLastName":
                self.userData["lastName"] = self.inputLastName.get_text()
                self.render[1] = self.font.render(self.userData["lastName"], True, (255, 255, 255))

            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "#inputState":
                self.userData["state"] = self.inputState.selected_option[0]
                self.render[2] = self.font.render(self.userData["state"], True, (255, 255, 255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputPassword":
                self.userData["password"] = self.inputPassword.get_text()
                self.render[3] = self.font.render(self.userData["password"], True, (255, 255, 255))

            if event.type == pgu.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#inputMail":
                self.userData["mail"] = self.inputMail.get_text()
                self.render[4] = self.font.render(self.userData["mail"], True, (255, 255, 255))

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonPlay":
                code = self.codeGenerator(self.userData)
                self.saveBinary(code)
                self.changePage(1)

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill((0,0,0))

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, data in enumerate(self.render):
            self.screen.blit(data, (50, 50*index))

    def backEnd(self):
        pass

    def codeGenerator(self, data:dict[str:str]):
        #hacerlo de forma recursiva
        return sum(ord(c) for c in data["name"]+data["lastName"]+data["state"]+data["password"]+data["mail"])
    
    def saveBinary(self, code:int):
        with open("./data/JUGADORES.bin", "rb") as file:
                info:list[bin] = file.readlines()

        with open("./data/JUGADORES.bin", "wb") as file:
            file.writelines(info)
            file.write(b"Code ")
            file.write(code.to_bytes(4))
            file.write(b"\n")
            for data in self.userData: file.write((data+"\n").encode())
    
    def bucle(self):
        self.events()
        self.frontEnd()
        self.backEnd()