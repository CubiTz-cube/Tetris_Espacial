import pygame as pg
import pygame_gui as pgu
from library.dynamicObjects import *
import globalVariables as gv
from library.dynamicObjects import DynamicButton

class Menu():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((W,H))
        self.isLoad = False

        self.buttonPlay = DynamicButton(300, 50, 150, 50, "Jugar", self.manager)
        self.buttonLeader = DynamicButton(300, 100, 150, 50, "Estadisticas", self.manager)
        self.buttonConfig = DynamicButton(300, 150, 150, 50, "Configuracion", self.manager)
        self.buttonExit = DynamicButton(300, 200, 150, 50, "Salir", self.manager)

        self.dynamicObjects = [
            DynamicRect(640, 0, 640, 720, "#FFFFFF"),
            self.buttonPlay,
            self.buttonLeader,
            self.buttonConfig,
            self.buttonExit
           
        ] 

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()

    def resetScreen(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)
        """self.resize()"""

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resize()
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
                gv.actualPage = 3
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLeader.element:
                gv.actualPage = 5
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonConfig.element:
                gv.actualPage = 6
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonExit.element:
                pg.quit()
                quit()

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill("#050611")

        for obj in self.dynamicObjects:
            obj.render()
        self.screen.fill((0,0,0))
        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def backEnd(self):
        pass

    def bucle(self):
        if not self.isLoad:
            self.resize()
            self.resetScreen()
            self.isLoad = True
        self.events()
        self.frontEnd()
        self.backEnd()