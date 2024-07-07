import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv
from library.dynamicObjects import *
import public.images.loadImages as img
from library.starsBack import StartMaker
from library.dynamicObjects import *

class GameOver():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\global.json")
        self.isLoad = False

        

        self.buttonReset = DynamicButton(640 - 150, 360 + 50, 370, 90, "", self.manager, ObjectID("", "@transparent"))
        self.imagenreiniciar = DynamicImage(640 - 150, 360 + 50, 0.4, img.buttons["reiniciar"])
        self.buttonMenu =  DynamicButton(640 - 145, 360 + 200, 370, 90, "", self.manager, ObjectID("", "@transparent"))
        self.imagenMenu = DynamicImage(640 - 150, 360 + 200, 0.4, img.buttons["menu"])
       
        

        self.textGameOver = DynamicText(210, 50, "JUEGO CONCLUIDO", gv.fontAldrich, 85, "#FFFFFF")
        self.textViewScore = DynamicText(840-pg.font.Font(gv.fontLektonBold, 45).size("Puntuación: ")[0], 140, "Puntuación: ", gv.fontLektonBold, 40, "#FFFFFF")
        
        self.dynamicObjects = [
            self.imagenMenu,
            self.imagenreiniciar,
            self.textGameOver,
            self.textViewScore,
            self.buttonReset,
            self.buttonMenu
        ]
        
        self.starts = StartMaker(50, 10, minSpeed = 0.5, maxSpeed = 1.5)
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.VIDEORESIZE:
                self.resize()
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonReset.element:
                gv.actualPage = 3
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == self.buttonReset.element:
                self.imagenreiniciar.changeImg(img.buttons["reiniciarHover"])
            if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == self.buttonReset.element:
                self.imagenreiniciar.changeImg(img.buttons["reiniciar"])
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonMenu.element:
                gv.actualPage = 2
                self.isLoad = False
            if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == self.buttonMenu.element:
                self.imagenMenu.changeImg(img.buttons["menuHover"])
            if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == self.buttonMenu.element:
                self.imagenMenu.changeImg(img.buttons["menu"])

            self.manager.process_events(event)

    def resize(self):
        self.buttonReset.resize()
        self.buttonMenu.resize()

        for obj in self.dynamicObjects:
            obj.resize()

        self.buttonReset.changeDimension(self.imagenreiniciar.image.get_width(), self.imagenreiniciar.image.get_height())
        self.buttonMenu.changeDimension(self.imagenMenu.image.get_width(), self.imagenMenu.image.get_height())

        self.starts.resize()

    def resetScreen(self):
        self.textViewScore.changeText(f"Puntuación: {gv.viewScore}")
        self.textViewScore.changeCoord(820 - pg.font.Font(gv.fontLektonBold, 45).size(self.textViewScore.text)[0], None)
        self.resize()
        pg.mouse.set_cursor(*pg.cursors.arrow)

    def frontEnd(self):
        self.screen.fill("#050611")

        
        self.starts.render()

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