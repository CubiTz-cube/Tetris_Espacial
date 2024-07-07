import pygame as pg
import pygame_gui as pgu

import globalVariables as gv
from library.dynamicObjects import *
from library.dataFormating import getAllUsers, quickSortScoreUser
from library.starsBack import StartMaker
import public.images.loadImages as img

class Leaderboard():
    def __init__(self) -> None:
        self.screen = pg.display.get_surface()
        self.clock = pg.Clock()
        W = pg.display.Info().current_w
        H = pg.display.Info().current_h
        self.manager = pgu.UIManager((gv.W,gv.W), "pages\\css\\global.json")
        self.manager.get_theme().load_theme("pages\\css\\leaderboard.json")
        self.isLoad = False

        self.showState = None
        self.showUser = None
        self.pageScore = 0
        self.pageAmount = 7
        self.isload = False

        self.textScores:list[DynamicText] = []
        for i in range(self.pageAmount):
            self.textScores.append(
                DynamicText(0, 50*i+200, f"Score {i+1}", gv.fontLekton, 28, "#FFFFFF")
            )

        self.textName = DynamicText(100, 24, gv.actualUser[2], gv.fontAldrich, 40, "#000000")
        self.textState = DynamicText(950, 24, gv.actualUser[3], gv.fontAldrich, 40, "#FFFFFF")

        self.buttonBack = DynamicButton(980, 650, 305, 80, "Regresar al menu", self.manager, ObjectID("#back",""))
        self.buttonNextScore = DynamicButton(1134, 600, 150, 50, "Siguiente", self.manager, ObjectID("#pages",""))
        self.buttonBackScore = DynamicButton(980, 600, 150, 50, "Anterior", self.manager, ObjectID("#pages",""))
        self.textPageScore = DynamicText(1076, 560, f"Página {self.pageScore+1}", gv.fontLekton, 28, "#FFFFFF")

        self.inputState = DynamicDropDown(0, 100, 300, 30, self.manager, gv.states)
        self.inputUser = DynamicDropDown(350, 100, 300, 30, self.manager, [("Usuario no seleccionado", None)]+[user[0] for user in getAllUsers()])
        
        self.dynamicObjects = [
            DynamicRect(0, -40, 10000, 120, "#FFFFFF"),
            DynamicRect(655, -40, 10000, 120, "#1C1C1C"),
            DynamicImage(0, 0, 0.070, img.logos["isotipoNegro"]),
            self.textName,
            self.textState,
            self.buttonBack,
            self.inputState,
            self.inputUser,
            self.buttonNextScore,
            self.buttonBackScore,
            self.textPageScore,
        ]

    def resize(self):
        for obj in self.dynamicObjects:
            obj.resize()
        for text in self.textScores:
            text.resize()

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
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputState.element:
                self.showState = self.inputState.element.selected_option[1]
                self.pageScore = 0
                self.updateLeaderboard()
            if event.type == pgu.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.inputUser.element:
                self.showUser = self.inputUser.element.selected_option[1]
                self.pageScore = 0
                self.updateLeaderboard()
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonNextScore.element:
                self.pageScore += 1
                self.updateLeaderboard()
                self.textPageScore.changeText(f"Página {self.pageScore+1}")
            if event.type == pgu.UI_BUTTON_PRESSED and event.ui_element == self.buttonBackScore.element:
                if self.pageScore > 0: self.pageScore -= 1
                self.updateLeaderboard()
                self.textPageScore.changeText(f"Página {self.pageScore+1}")

            self.manager.process_events(event)
    
    def resetScreen(self):
        self.isload = True
        self.resize()
        self.pageScore = 0
        self.updateLeaderboard()
        self.textName.changeText(gv.actualUser[2])
        self.textState.changeText(gv.actualUser[3])

    def updateLeaderboard(self):
        for i in range(self.pageAmount):
            self.textScores[i].changeText("")

        users = self.filterState(getAllUsers(),self.showState)
        users = self.filterUser(users, self.showUser)

        scoreList = []
        for user in users:
            for score in user[4]:
                scoreList.append((score,user[3],user[2]))

        # Formato ejemplo ([300, 5, 6, 2024, 8, 44], 'Bolívar', 'Juan')
        scoreList = quickSortScoreUser(scoreList)

        startIndex = self.pageAmount*self.pageScore
        endIndex = self.pageAmount*(self.pageScore+1)

        if len(scoreList[startIndex:endIndex]) < 1:
            self.pageScore -= 1
            startIndex = self.pageAmount*self.pageScore
            endIndex = self.pageAmount*(self.pageScore+1)
            scoreList = []
            for user in users:
                for score in user[4]:
                    scoreList.append((score,user[3],user[2]))
            scoreList = quickSortScoreUser(scoreList)

        for i, score in enumerate(scoreList[startIndex:endIndex]):
            text = f"• {score[0][0]} | {score[2]} - {score[1]} | Fecha: {score[0][1]}/{score[0][2]}/{score[0][3]} | Hora: {score[0][4]}:{score[0][5]}"
            self.textScores[i].changeText(text)

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
        self.screen.fill("#050611")

        for text in self.textScores:
            text.render()

        for obj in self.dynamicObjects:
            obj.render()

        self.manager.update(self.clock.tick(60)/1000)
        self.manager.draw_ui(self.screen)

    def bucle(self):
        if not self.isload:
            self.resetScreen()

        self.frontEnd()
        self.events()