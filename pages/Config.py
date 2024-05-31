import pygame as pg
import pygame_gui as pgu

import globalVariables as gv

class Config():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Inicar juego con el tablero actual",
        manager=self.manager,
        object_id="#buttonPlay")

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonPlay":
                gv.actualPage = 4

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