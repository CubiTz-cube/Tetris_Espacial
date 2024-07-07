import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv
from library.dynamicObjects import *
import public.sonds.loadSonds as sonds
import public.images.loadImages as img
from library.starsBack import StartMaker

class Config():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\global.json")
        self.manager.get_theme().load_theme("pages\\css\\config.json")
        self.isload = False

        self.textName = DynamicText(100, 24, gv.actualUser[2], gv.fontAldrich, 40, "#000000")
        self.textState = DynamicText(950, 24, gv.actualUser[3], gv.fontAldrich, 40, "#FFFFFF")

        self.buttonBack = DynamicButton(980, 650, 305, 80, "Regresar al menu", self.manager, ObjectID("#back",""))

        self.textSpeed = DynamicText(200, 260, "Velocidad: ", gv.fontLekton, 40, "#FFFFFF")
        self.InputSpeed = DynamicInput(450, 250, 350, 60, self.manager, str(gv.speed*100))
        self.buttonMusic = DynamicButton(650, 350, 350, 60, "Mutear Musica" if gv.music else "Activar Musica", self.manager, ObjectID("#ButtonConfig",""))
        self.buttonMusicChange = DynamicButton(200, 350, 350, 60, "Cambiar Musica", self.manager, ObjectID("#ButtonConfig",""))
        self.buttonPiecesNum = DynamicButton(375, 450, 450, 60, "Piezas con números" if gv.piecesHasNum else "Piezas sin números", self.manager, ObjectID("#ButtonConfig",""))

        self.dynamicObjects = [
            DynamicRect(0, -40, 10000, 120, "#FFFFFF"),
            DynamicRect(655, -40, 10000, 120, "#1C1C1C"),
            DynamicImage(0, 0, 0.070, img.logos["isotipoNegro"]),
            self.textName,
            self.textState,
            self.buttonBack,
            self.textSpeed,
            self.InputSpeed,
            self.buttonMusic,
            self.buttonMusicChange,
            self.buttonPiecesNum,
        ]

        self.starts = StartMaker(50, 10, minSpeed = 0.5, maxSpeed = 1)

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()
        
        self.starts.resize()

    def resetScreen(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)
        self.resize()
        self.textName.changeText(gv.actualUser[2])
        self.textState.changeText(gv.actualUser[3])
        self.isload = True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.VIDEORESIZE:
                self.resize()
                pass

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBack.element:
                gv.actualPage = 2
                self.isload = False

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonMusicChange.element:
                gv.actualSong = (gv.actualSong + 1) % len(sonds.music)
                sonds.playMusic(sonds.music[gv.actualSong])

            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonMusic.element:
                if gv.music:
                    self.buttonMusic.element.set_text("Activar Musica")
                    gv.music = False
                    sonds.stopMusic()
                else:
                    self.buttonMusic.element.set_text("Mutear Musica")
                    gv.music = True
                    sonds.playMusic(sonds.music[gv.actualSong])
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPiecesNum.element:
                if gv.piecesHasNum:
                    self.buttonPiecesNum.element.set_text("Piezas sin números")
                    gv.piecesHasNum = False
                else:
                    self.buttonPiecesNum.element.set_text("Piezas con números")
                    gv.piecesHasNum = True

            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.InputSpeed.element:
                newSpeed = self.InputSpeed.element.get_text()
                try:
                    newSpeed = abs(int(newSpeed))
                    if newSpeed > 1000:
                        newSpeed = 1000
                        self.InputSpeed.element.set_text("1000")
                    gv.speed = 1 * (newSpeed/100)
                except:
                    pass


            self.manager.process_events(event)

    def frontEnd(self):
        self.screen.fill("#050611")

        self.starts.render()

        for obj in self.dynamicObjects:
            obj.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def bucle(self):
        if not self.isload:
            self.resetScreen()

        self.events()
        self.frontEnd()