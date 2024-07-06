import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

import public.images.loadImages as img
from library.dynamicObjects import *

class Intro():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\global.json")
        self.isLoad = False

        self.icon = DynamicImage(370, 80, 0.5, img.logos["imagoTipoColor"])
        self.alfa = 4

        self.dynamicObjects = [
            self.icon,
        ]

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                self.resize()
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                gv.actualPage = 0

            self.manager.process_events(event)

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()

    def bucle(self):
        self.screen.fill("#000000")
        self.icon.changeAlfa(self.alfa)
        self.alfa *= 1.02

        for text in self.dynamicObjects:
            text.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        if self.alfa > 300:
            gv.actualPage = 0

        self.events()