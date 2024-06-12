import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID

import globalVariables as gv
import public.images.loadImages as img
from library.piece import allPieces, imgCompletePiecesNum
from library.imageEdit import convertImgToBn

class Selection():
    def __init__(self) -> None:

        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H), "pages\\css\\selection.json")

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Iniciar",
        manager=self.manager)

        self.buttonBack = pgu.elements.UIButton(
        relative_rect=pg.Rect((100, 50), (150, 50)),
        text="Regresar",
        manager=self.manager)

        self.inputMode = pgu.elements.UIDropDownMenu(
        relative_rect=pg.Rect((300, 100), (150, 30)),
        starting_option="Desactivado",
        options_list=["Desactivado", "Tiempo", "Pieza"],
        manager=self.manager)

        self.inputLimit = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((300, 150), (150, 30)),
        initial_text="0",
        manager=self.manager)

        self.inputDimX = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((350, 200), (100, 30)),
        initial_text="12",
        manager=self.manager)

        self.inputDimY = pgu.elements.UITextEntryLine(
        relative_rect=pg.Rect((250, 200), (100, 30)),
        initial_text="21",
        manager=self.manager)

        self.pieceButtons:list[pgu.elements.UIButton] = []
        self.pieceImages:list[pgu.elements.UIImage] = []
        for i in range(len(imgCompletePiecesNum)):
            imageSize = imgCompletePiecesNum[i].get_size()
            self.pieceButtons.append(pgu.elements.UIButton(
            relative_rect=pg.Rect((100 + 100 * i, 250), (imageSize[0]//2,imageSize[1]//2)),
            text="",
            manager=self.manager,
            object_id= ObjectID("#select","@transparent"),
            ))
            self.pieceImages.append(pgu.elements.UIImage(
            relative_rect=pg.Rect((100 + 100 * i, 250), (imageSize[0]//2,imageSize[1]//2)),
            image_surface=imgCompletePiecesNum[i],
            manager=self.manager))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                gv.actualPage = 4
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBack:
                gv.actualPage = 2
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputMode:
                if self.inputMode.selected_option[0] == "Desactivado": 
                    gv.limit = 0
                    gv.mode = 0
                if self.inputMode.selected_option[0] == "Tiempo": 
                    gv.limit = 60
                    gv.mode = 1
                if self.inputMode.selected_option[0] == "Pieza": 
                    gv.limit = 10
                    gv.mode = 2
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputLimit:
                try:
                    gv.limit = int(self.inputLimit.get_text())
                except:
                    pass
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputDimX:
                try:
                    change = int(self.inputDimX.get_text())
                    if change % 3 == 0 and change > 9: gv.dimX = change
                    else: print("dimX no es multiplo de 3 mayor que 9")
                except:
                    pass
            if event.type == pgu.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.inputDimY:
                try:
                    change = int(self.inputDimY.get_text())
                    if change % 3 == 0 and change > 9: gv.dimX = change
                    else: print("dimY no es multiplo de 3 mayor que 9")
                except:
                    pass

            for index, button in enumerate(self.pieceButtons):
                if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == button:
                    if  "#unSelect" in button.get_object_ids():
                        button.change_object_id(ObjectID("#select","@transparent"))
                        gv.activePieces[index] = True
                        self.pieceImages[index].set_image(imgCompletePiecesNum[index])
                    elif gv.activePieces.count(True) > 5:
                        button.change_object_id("#unSelect")
                        gv.activePieces[index] = False
                        self.pieceImages[index].set_image(convertImgToBn(imgCompletePiecesNum[index]))

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