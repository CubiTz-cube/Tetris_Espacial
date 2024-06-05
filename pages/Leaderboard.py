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
        self.textRenderDataLeader:list[pg.font.Font] = []

        self.buttonPlay = pgu.elements.UIButton(
        relative_rect=pg.Rect((300, 50), (150, 50)),
        text="Regresar al menu",
        manager=self.manager)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonPlay:
                gv.actualPage = 2
                self.isLoad = False

            self.manager.process_events(event)
    def showLeaderboard(self, estado:str = "", fecha:str = ""):
        if not self.isLoad:
            self.textRenderDataLeader = []
            for user in getAllUsers(gv.fileUsers):
                for score in user[4]:
                    self.textRenderDataLeader.append(pg.font.Font(gv.fontLekton, 32).render(f"{user[2]} - {score[3]}", True, (255,255,255)))
            self.isLoad = True
        
        for index, text in enumerate(self.textRenderDataLeader):
            self.screen.blit(text, (self.W//2 - text.get_width()//2, 50*index))

    def frontEnd(self):
        self.screen.fill((0,0,0))
        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

        self.showLeaderboard()

    def backEnd(self):
        pass

    def bucle(self):
        self.frontEnd()
        self.backEnd()
        self.events()