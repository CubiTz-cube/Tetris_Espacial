import pygame as pg
import pygame_gui as pgu

import globalVariables as gv

from library.dataFormating import getAllUsers

class Leaderboard():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        self.W = pg.display.Info().current_w
        self.H = pg.display.Info().current_h
        self.manager = pgu.UIManager((self.W,self.H))

        self.isLoad = False
        self.showState = "Bolívar"
        self.textRenderDataLeader:list[pg.font.Font] = []

        self.buttonBack = pgu.elements.UIButton(
            relative_rect=pg.Rect((300, 50), (150, 50)),
            text="Regresar al menu",
            manager=self.manager)

        self.inputState = pgu.elements.UIDropDownMenu(
            relative_rect=pg.Rect((250, 100), (500, 30)),
            starting_option="Bolívar",
            options_list=gv.states,
            manager=self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBack:
                gv.actualPage = 2
                self.isLoad = False
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState:
                self.isLoad = False
                self.showState = self.inputState.selected_option[0]

            self.manager.process_events(event)
    def showLeaderboard(self, estado:str = "", fecha:list[int] = []	):
        if not self.isLoad:
            self.textRenderDataLeader = []
            for user in getAllUsers(gv.fileUsers):
                for score in user[4]:
                    text = f"{user[3]} - {user[2]} - {score[0]}"
                    if estado == "" and fecha == "":
                        self.textRenderDataLeader.append(pg.font.Font(gv.fontLekton, 32).render(text, True, (255,255,255)))
                    elif estado == "":
                        pass
                    elif fecha == []:
                        if user[3] == estado:
                            self.textRenderDataLeader.append(pg.font.Font(gv.fontLekton, 32).render(text, True, (255,255,255)))
                    else:
                        pass

            self.isLoad = True
        
        for index, text in enumerate(self.textRenderDataLeader):
            self.screen.blit(text, (self.W//2 - text.get_width()//2, 50*index))

    def frontEnd(self):
        self.screen.fill((0,0,0))
        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        self.showLeaderboard(estado=self.showState)

    def backEnd(self):
        pass

    def bucle(self):
        self.frontEnd()
        self.backEnd()
        self.events()