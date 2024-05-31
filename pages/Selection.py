import pygame as pg
import pygame_gui as pgu

import globalVariables as gv

class Selection():
    def __init__(self, changePage) -> None:
        self.changePage = changePage

        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Inicar",
        manager=self.manager,
        object_id="#buttonPlay")

        self.inputModo = pgu.elements.UIDropDownMenu(
        relative_rect=pg.Rect((300, 150), (150, 30)),
        starting_option="Desactivado",
        options_list=["Desactivado", "Tiempo", "Pieza"],
        manager=self.manager,
        object_id="#inputModo")

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonPlay":
                self.changePage(4)
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "#inputModo":
                if self.inputModo.selected_option[0] == "Desactivado": 
                    gv.limit = 0
                    gv.mode = 0
                if self.inputModo.selected_option[0] == "Tiempo": 
                    gv.limit = 60
                    gv.mode = 1
                if self.inputModo.selected_option[0] == "Pieza": 
                    gv.limit = 10
                    gv.mode = 2

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill((0,0,0))
        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def backEnd(self):
        pass

    def bucle(self):
        self.events()
        self.frontEnd()
        self.backEnd()