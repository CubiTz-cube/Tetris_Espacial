import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

import public.images.loadImages as img
from library.dynamicObjects import *

class GameOver():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((W,H), "pages\\css\\global.json")
        self.isLoad = False

        self.buttonReset = DynamicButton(640 - 180, 360 + 100, 360, 70, "Reiniciar", self.manager)
        self.buttonMenu = DynamicButton(640 - 180, 360 + 200, 360, 70, "Menu", self.manager)

        self.textGameOver = DynamicText(240, 20, "JUEGO CONCLUIDO", gv.fontAldrich, 85, "#FFFFFF")
        self.textViewScore = DynamicText(840-pg.font.Font(gv.fontLektonBold, 45).size("Puntuación: ")[0], 140, "Puntuación: ", gv.fontLektonBold, 45, "#FFFFFF")
        self.dynamicObjects = [
            self.textGameOver,
            self.textViewScore
        ]

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resize()
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonReset.element:
                gv.actualPage = 3
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonMenu.element:
                gv.actualPage = 2
                self.isLoad = False

            self.manager.process_events(event)

    def resize(self):
        self.buttonReset.resize()
        self.buttonMenu.resize()

        for obj in self.dynamicObjects:
            obj.resize()

    def resetScreen(self):
        self.textViewScore.changeText(f"Puntuación: {gv.viewScore}")
        self.textViewScore.changeCoord(840 - pg.font.Font(gv.fontLektonBold, 45).size(self.textViewScore.text)[0], None)
        self.resize()
        pg.mouse.set_cursor(*pg.cursors.arrow)

    def frontEnd(self):
        self.screen.fill("#050611")

        for text in self.dynamicObjects:
            text.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)
    
    def bucle(self):
        if not self.isLoad:
            self.resetScreen()
            self.isLoad = True

        self.frontEnd()
        self.events()