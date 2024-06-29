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

        self.showState = None
        self.showUser = None
        self.textRenderDataLeader:list[pg.font.Font] = []
        self.updateLeaderboard()

        self.buttonBack = pgu.elements.UIButton(
            relative_rect=pg.Rect((300, 50), (150, 50)),
            text="Regresar al menu",
            manager=self.manager)

        self.inputState = pgu.elements.UIDropDownMenu(
            relative_rect=pg.Rect((250, 100), (500, 30)),
            starting_option=("Ninguno", None),
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
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState:
                self.showState = self.inputState.selected_option[1]
                self.updateLeaderboard()

            self.manager.process_events(event)
    
    def updateLeaderboard(self):
        self.textRenderDataLeader = []
        scores = self.filterState(getAllUsers(),self.showState)
        scores = self.filterUser(scores, self.showUser)

        for user in scores:
            for score in user[4]:
                text = f"{user[3]} - {user[2]} Puntos: {score[0]} fecha: {score[1]}/{score[2]}/{score[3]} Hora: {score[4]}:{score[5]}"
                self.textRenderDataLeader.append(pg.font.Font(gv.fontLekton, 32).render(text, True, (255,255,255)))

    def filterState(self, users:list[list],state:str):
        if state == None: return users

        newList = []
        for user in users:
            stateUser = user[3]
            if stateUser == state:
                newList.append(user)
        return newList

    def filterUser(self, users:list[list], mail:str):
        if mail == None: return users

        newList = []
        for user in users:
            mailUser = user[0]
            if mailUser == mail:
                newList.append(user)
        return newList

    def frontEnd(self):
        self.screen.fill((0,0,0))
        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        for index, text in enumerate(self.textRenderDataLeader):
            self.screen.blit(text, (self.W//2 - text.get_width()//2, (50*index)+150))

    def backEnd(self):
        pass

    def bucle(self):
        self.frontEnd()
        self.backEnd()
        self.events()