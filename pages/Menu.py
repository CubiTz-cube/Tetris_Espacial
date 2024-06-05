import pygame as pg
import pygame_gui as pgu

import globalVariables as gv

class Menu():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Jugar",
        manager=self.manager)

        self.buttonLeader = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 100), (150, 50)),
        text="Estadisticas",
        manager=self.manager)

        self.buttonConfig = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 150), (150, 50)),
        text="Configuracion",
        manager=self.manager)

        self.buttonExit = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 200), (150, 50)),
        text="Salir",
        manager=self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                gv.actualPage = 3
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLeader:
                gv.actualPage = 5
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonConfig:
                gv.actualPage = 6
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonExit:
                pg.quit()
                quit()

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