import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv

from library.dynamicObjects import *
from library.starsBack import StartMaker
import public.images.loadImages as img

class Menu():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\global.json")
        self.isLoad = False

        self.textName = DynamicText(100, 24, gv.actualUser[2], gv.fontAldrich, 40, "#000000")
        self.textState = DynamicText(950, 24, gv.actualUser[3], gv.fontAldrich, 40, "#FFFFFF")

        self.buttonPlay = DynamicButton(0, 125, 730, 130, "", self.manager, ObjectID("", "@transparent"))
        self.imageButtonPlay = DynamicImage(0, 125, 0.6, img.buttons["play"])

        self.buttonLeader = DynamicButton(0, 300, 730, 130, "", self.manager, ObjectID("", "@transparent"))
        self.imageButtonLeader = DynamicImage(0, 300, 0.6, img.buttons["rank"])

        self.buttonConfig = DynamicButton(0, 480, 730, 130, "", self.manager, ObjectID("", "@transparent"))
        self.imageButtonConfig = DynamicImage(0, 480, 0.6, img.buttons["config"])

        self.dynamicObjects = [
            DynamicRect(0, -40, 10000, 120, "#FFFFFF"),
            DynamicRect(655, -40, 10000, 120, "#1C1C1C"),
            DynamicImage(0, 0, 0.070, img.logos["isotipoNegro"]),
            self.buttonPlay,
            self.buttonLeader,
            self.buttonConfig,
            self.imageButtonPlay,
            self.imageButtonLeader,
            self.imageButtonConfig,
            self.textName,
            self.textState,
        ] 

        self.starts = StartMaker(50, 10, minSpeed = 0.5, maxSpeed = 1.5)

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()

        self.buttonPlay.changeDimension(self.imageButtonPlay.image.get_width(), self.imageButtonPlay.image.get_height())
        self.buttonLeader.changeDimension(self.imageButtonLeader.image.get_width(), self.imageButtonLeader.image.get_height())
        self.buttonConfig.changeDimension(self.imageButtonConfig.image.get_width(), self.imageButtonConfig.image.get_height())

        self.starts.resize()

    def resetScreen(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)
        self.resize()
        self.textName.changeText(gv.actualUser[2])
        self.textState.changeText(gv.actualUser[3])

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                gv.running = False
            if event.type == pg.VIDEORESIZE:
                self.resize()
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
                gv.actualPage = 3
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == self.buttonPlay.element:
                self.imageButtonPlay.changeImg(img.buttons["playHover"])
            if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == self.buttonPlay.element:
                self.imageButtonPlay.changeImg(img.buttons["play"])

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonLeader.element:
                gv.actualPage = 5
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == self.buttonLeader.element:
                self.imageButtonLeader.changeImg(img.buttons["rankHover"])
            if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == self.buttonLeader.element:
                self.imageButtonLeader.changeImg(img.buttons["rank"])

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonConfig.element:
                gv.actualPage = 6
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == self.buttonConfig.element:
                self.imageButtonConfig.changeImg(img.buttons["configHover"])
            if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == self.buttonConfig.element:
                self.imageButtonConfig.changeImg(img.buttons["config"])

            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill("#050611")

        self.starts.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for obj in self.dynamicObjects:
            obj.render()

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