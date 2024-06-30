import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv
from library.dynamicObjects import DynamicInput, DynamicButton

class Config():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.buttonBack = DynamicButton(300, 50, 150, 50, "Regresar al menu", self.manager)

        self.InputSpeed = DynamicInput(300, 150, 150, 30, self.manager, str(gv.speed*100))
        self.buttonMusic = DynamicButton(500, 150, 150, 30, "Mutear Musica", self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.VIDEORESIZE:
                #Resize screen
                pass

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBack.element:
                gv.actualPage = 2

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonMusic.element:
                if gv.music:
                    self.buttonMusic.element.set_text("Activar Musica")
                    gv.music = False
                else:
                    self.buttonMusic.element.set_text("Mutear Musica")
                    gv.music = True

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