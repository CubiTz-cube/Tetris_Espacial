import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv
import public.images.loadImages as img
from library.dynamicObjects import *
from library.piece import allPieces, imgCompletePiecesNum
from library.imageEdit import *
from library.starsBack import StartMaker

class Selection():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\selection.json")
        self.manager.get_theme().load_theme("pages\\css\\global.json")
        self.isLoad = False

        self.backGround = DynamicRect(0, 450, 1280, 270, "#FFFFFF")

        self.textDimension = DynamicText(155, 470, "Dimensiones", gv.fontLekton, 28, "#1C1C1C")

        self.boxDimX = DynamicRect(133, 520, 200, 40, "#FFFFFF", 3, "#1C1C1C")
        self.textValueDimX = DynamicText(220, 526, str(gv.dimX), gv.fontLekton, 28, "#1C1C1C")
        self.buttonDimXR = DynamicButton(325, 514, 40, 50, "+", self.manager, ObjectID("#plus",""))
        self.buttonDimXL = DynamicButton(100, 514, 40, 50, "-", self.manager, ObjectID("#less",""))
        self.textX = DynamicText(70, 526, "X", gv.fontLekton, 32, "#1C1C1C")

        self.boxDimY = DynamicRect(133, 585, 200, 40, "#FFFFFF", 3, "#1C1C1C")
        self.textValueDimY = DynamicText(220, 592, str(gv.dimY), gv.fontLekton, 28, "#1C1C1C")
        self.buttonDimYR = DynamicButton(325, 580, 40, 50, "+", self.manager, ObjectID("#plus",""))
        self.buttonDimYL = DynamicButton(100, 580, 40, 50, "-", self.manager, ObjectID("#less",""))
        self.textY = DynamicText(70, 592, "Y", gv.fontLekton, 32, "#1C1C1C")

        self.textMode = DynamicText(920, 470, "Modo", gv.fontLekton, 28, "#1C1C1C")
        self.inputMode = DynamicDropDown(875, 514, 150, 40, self.manager, ["Desactivado", "Tiempo", "Pieza"], "Desactivado")

        self.textLimit = DynamicText(1120, 470, "Limite", gv.fontLekton, 28, "#000000")
        self.inputLimit = DynamicInput(1085, 514, 150, 40, self.manager, str(gv.limit))

        self.buttonPlay = DynamicButton(460, 590, 360, 120, "Iniciar", self.manager, ObjectID("#play",""))
        self.buttonBack = DynamicButton(980, 650, 305, 80, "Regresar al menu", self.manager, ObjectID("#back",""))

        self.TextSelection = DynamicText(35, 10, "Seleccion de piezas", gv.fontAldrich, 32, "#FFFFFF")
        self.buttonClasic = DynamicButton(400, 0, 200, 50, "Clasico", self.manager, ObjectID("#selectPiece",""))
        self.buttonRequest = DynamicButton(600, 00, 200, 50, "Pedido", self.manager, ObjectID("#selectPiece",""))

        self.dinamicObjects = [
            self.backGround,
            self.TextSelection,
            self.buttonPlay,
            self.buttonBack, 
            self.textMode,
            self.inputMode, 
            self.textLimit,
            self.inputLimit,

            self.textDimension,

            self.boxDimX,
            self.textValueDimX,
            self.buttonDimXR,
            self.buttonDimXL,
            self.textX,

            self.boxDimY,
            self.textValueDimY, 
            self.buttonDimYR,
            self.buttonDimYL,
            self.textY,

            self.buttonClasic,
            self.buttonRequest,
        ]

        self.pieceImages:list[DynamicImage] = []
        self.pieceButtons:list[DynamicButton] = []
        for i in range(len(imgCompletePiecesNum)):
            self.pieceImages.append(
                DynamicImage(50+105*i, 200, 0.5, imgCompletePiecesNum[i])
            )
            self.pieceButtons.append(
                DynamicButton(50+105*i, 200, 100, 100, "", self.manager, ObjectID("#select","@transparent"))
            )
        
        for i in range(len(self.pieceImages)):
            self.pieceButtons[i].changeDimension(self.pieceImages[i].image.get_width(), self.pieceImages[i].image.get_height())

        self.starts = StartMaker(50, 10, minSpeed = 0.5, maxSpeed = 1)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                
                gv.running = False
            if event.type == pg.VIDEORESIZE:
                self.resize()
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay.element:
                gv.actualPage = 4
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBack.element:
                gv.actualPage = 2
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputMode.element:
                if self.inputMode.element.selected_option[0] == "Desactivado": 
                    gv.limit = 0
                    gv.mode = 0
                if self.inputMode.element.selected_option[0] == "Tiempo": 
                    gv.mode = 1
                if self.inputMode.element.selected_option[0] == "Pieza": 
                    gv.mode = 2
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputLimit.element:
                try:
                    gv.limit = int(self.inputLimit.element.get_text())
                except:
                    pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonDimXL.element:
                if gv.dimX > 9:
                    gv.dimX -= 3
                    self.textValueDimX.changeText(str(gv.dimX))
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonDimXR.element:
                if gv.dimX < 30:
                    gv.dimX += 3
                    self.textValueDimX.changeText(str(gv.dimX))
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonDimYL.element:
                if gv.dimY > 9:
                    gv.dimY -= 3
                    self.textValueDimY.changeText(str(gv.dimY))
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonDimYR.element:
                if gv.dimY < 42:
                    gv.dimY += 3
                    self.textValueDimY.changeText(str(gv.dimY))
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonClasic.element:
                gv.activePieces = [False, False, True, True, True, False, True, False, False, True, True, True]
                for i, active in enumerate(gv.activePieces):
                    if active:
                        self.pieceButtons[i].element.change_object_id(ObjectID("#select","@transparent"))
                        self.pieceImages[i].changeImg(imgCompletePiecesNum[i])
                    else:
                        self.pieceButtons[i].element.change_object_id("#unSelect")
                        self.pieceImages[i].changeImg(convertImgToBn(imgCompletePiecesNum[i]))
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonRequest.element:
                gv.activePieces = [True, True, True, True, True, True, True, True, True, False, False, False]
                for i, active in enumerate(gv.activePieces):
                    if active:
                        self.pieceButtons[i].element.change_object_id(ObjectID("#select","@transparent"))
                        self.pieceImages[i].changeImg(imgCompletePiecesNum[i])
                    else:
                        self.pieceButtons[i].element.change_object_id("#unSelect")
                        self.pieceImages[i].changeImg(convertImgToBn(imgCompletePiecesNum[i]))

            for index, button in enumerate(self.pieceButtons):
                if event.type == pgu.UI_BUTTON_ON_HOVERED and event.ui_element == button.element:
                    self.pieceImages[index].changeImg(lightImage(self.pieceImages[index].imageSave, 35))

                if event.type == pgu.UI_BUTTON_ON_UNHOVERED and event.ui_element == button.element:
                    if gv.activePieces[index]:
                        self.pieceImages[index].changeImg(imgCompletePiecesNum[index])
                    else:
                        self.pieceImages[index].changeImg(convertImgToBn(imgCompletePiecesNum[index]))

                if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == button.element:
                    if  "#unSelect" in button.element.get_object_ids():
                        button.element.change_object_id(ObjectID("#select","@transparent"))
                        gv.activePieces[index] = True
                        self.pieceImages[index].changeImg(imgCompletePiecesNum[index])
                    elif gv.activePieces.count(True) > 5:
                        button.element.change_object_id("#unSelect")
                        gv.activePieces[index] = False
                        self.pieceImages[index].changeImg(convertImgToBn(imgCompletePiecesNum[index]))

            self.manager.process_events(event)
    
    def resetScreen(self):
        self.resize()

    def resize(self):
        for obj in self.dinamicObjects:
            obj.resize()

        for img in self.pieceImages:
            img.resize()

        for i in range(len(self.pieceImages)):
            self.pieceButtons[i].resize()
            self.pieceButtons[i].changeDimension(self.pieceImages[i].image.get_width(), self.pieceImages[i].image.get_height())
        
        self.starts.resize()

    def frontEnd(self):
        self.screen.fill("#050611")

        self.starts.render()

        for obj in self.dinamicObjects:
            obj.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for img in self.pieceImages:
            img.render()

    def bucle(self):
        if not self.isLoad:
            self.resetScreen()
            self.isLoad = True

        self.events()
        self.frontEnd()