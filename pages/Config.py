import pygame as pg
import pygame_gui as pgu

import globalVariables as gv
from library.dynamicObjects import DynamicInput

class Config():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Regresar al menu",
        manager=self.manager,
        object_id="#buttonPlay")

        self.InputSpeed = DynamicInput(300, 150, 150, 30, self.manager, str(gv.speed*100))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.VIDEORESIZE:
                #Resize screen
                pass

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_object_id == "#buttonPlay":
                gv.actualPage = 2

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.InputSpeed.element:
                newSpeed = self.InputSpeed.element.get_text()
                try:
                    newSpeed = int(newSpeed)
                    gv.speed = 1 * (newSpeed/100)
                    print(f"nueva velocidad {gv.speed}")
                except:
                    pass


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