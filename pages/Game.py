import pygame as pg
import numpy as np

import library.piece as piece
import public.images.loadImages as img
from library.starsBack import StartMaker
import library.dataFormating as df
import globalVariables as gv

from random import choice
from copy import copy

class Game():
    def __init__(self):
        self.board = np.full([gv.dimY,gv.dimX], 0)
        self.pieces = []
        for index,active in enumerate(gv.activePieces):
            if active:
                self.pieces.append(piece.allPieces[index])
                
        #[piezaIvar, piezaI, piezaL, piezaLI, piezaS, piezaLvar, piezaO, piezaT, piezaTvar] piezas que pode franklin
        #[piezaImax, piezaTmin, piezaO, piezaS, piezaSI, piezaL, piezaLI] Piezas clasicas de tetris

        self.piecesImg = {pieza.value:pieza.image for pieza in self.pieces}

        self.lastTime = pg.time.get_ticks()
        self.screen = pg.display.get_surface()
        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]
        self.isLoad = False
        self.start_time = pg.time.get_ticks()

        self.gameOverScene = False
 
        self.pieceInGame = [copy(choice(self.pieces)) for _ in range(2)]
        self.score = 0
        self.tickPiece = 0
        self.tickKey = 0
        self.move = [0,0]

        self.textRenderNumber = [pg.font.Font(gv.fontLekton, 30).render(f"{i-2}", True, (0,0,0)) for i in range(2,15)]
        self.textRenderModeInactive = pg.font.Font(gv.fontLekton, 30).render(f"Sin modo de juego", True, (255,255,255))
        self.textRenderModeTime = pg.font.Font(gv.fontLekton, 30).render(f"Tiempo restante:", True, (255,255,255))
        self.textRenderModePiece = pg.font.Font(gv.fontLekton, 30).render(f"Piezas restantes:", True, (255,255,255))
        self.scoreTextRender = pg.font.Font(gv.fontLekton, 30).render(f"Score: {self.score}", True, (255,255,255))
        self.textRenderLimit = pg.font.Font(gv.fontLekton, 30).render(f"{gv.limit}", True, (255,255,255))

        self.TIMEREVENT = pg.USEREVENT + 2
        pg.time.set_timer(self.TIMEREVENT, 1000)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.VIDEORESIZE:
                #Reside screen
                pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.pieceInGame[0].move(self.board,[-1,0])
                    self.move = [-1,0]
                    self.tickKey = 0
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.pieceInGame[0].move(self.board,[1,0])
                    self.move = [1,0]
                    self.tickKey = 0
                elif event.key == pg.K_SPACE:
                    while not self.pieceInGame[0].static:
                        self.pieceInGame[0].move([0,1])
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.pieceInGame[0].move(self.board,[0,1])
                    self.move = [0,1]
                    self.tickKey = 0
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    self.pieceInGame[0].rotateR(self.board)
                elif event.key == pg.K_ESCAPE:
                    self.isLoad = False
                    gv.actualPage = 2
            if event.type == pg.KEYUP:
                self.move = [0,0]
            if event.type == self.TIMEREVENT:
                if gv.mode == 1:
                    gv.limit -= 1
                    self.textRenderLimit = pg.font.Font(gv.fontLekton, 30).render(f"{gv.limit}", True, (255,255,255))
                    if gv.limit <= 0: self.gameOver()
            
    def resetGame(self):
        self.board = np.full([gv.dimY,gv.dimX,4], [0, 0, 0, 0])
        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]
        self.score = 0
        self.tickPiece = 0
        self.tickKey = 0
        self.move = [0,0]
        self.pieces = []
        for index,active in enumerate(gv.activePieces): 
            if active:
                self.pieces.append(piece.allPieces[index])
        self.pieceInGame = [copy(choice(self.pieces)) for _ in range(2)]
        self.textRenderLimit = pg.font.Font(gv.fontLekton, 30).render(f"{gv.limit}", True, (255,255,255))
        
    def checkModePieza(self):
        if gv.mode == 2:
            gv.limit -= 1
            self.textRenderLimit = pg.font.Font(gv.fontLekton, 30).render(f"{gv.limit}", True, (255,255,255))
        if gv.limit <= 0: self.gameOver()
    
    def checkModeTiempo(self):
        pg.time.set_timer(pg.USEREVENT, 1000)
        if gv.mode == 1:
            self.textRenderLimit = pg.font.Font(gv.fontLekton, 30).render(f"{gv.limit}", True, (255,255,255))

    def gameOver(self):
        #self.gameOverScene = True
        df.addUserScore()
        exit()

    def drawBackground(self):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen, (255,255,255), (0, 0, self.dimX *30, (self.dimY-3) * 30))

    def drawText(self):
        self.screen.blit(self.textRenderLimit, (670, 150))
        self.screen.blit(self.scoreTextRender, (400, 100))
        if gv.mode == 0: self.screen.blit(self.textRenderModeInactive, (400, 150))
        elif gv.mode == 1: self.screen.blit(self.textRenderModeTime, (400, 150))  
        else: self.screen.blit(self.textRenderModePiece, (400, 150))

    def drawPieces(self):
        for Y in range(3, self.dimY):
            for X in range(self.dimX):
                if self.board[Y,X][0] != 0:
                    image = self.piecesImg[self.board[Y,X][0]]
                    image = pg.transform.scale(image, (31,31))
                    self.screen.blit(image, (X * 30, (Y-3) * 30))
                    self.screen.blit(self.textRenderNumber[self.board[Y,X][0]], (X * 30, (Y-3) * 30))
                elif self.pieceInGame[0].x in [X,X-1,X-2]:
                    pg.draw.rect(self.screen, (240,240,240), (X * 30, (Y-3) * 30, 30, 30))

    def drawUI(self):

        for Y in range(3):
            for X in range(3):
                if self.pieceInGame[1].shape[Y,X] != 0:
                    #pg.draw.rect(self.screen, self.pieceInGame[1].color, (400 + X * 30, Y * 30, 30, 30))
                    image = self.piecesImg[self.pieceInGame[1].value]
                    image = pg.transform.scale(image, (31,31))
                    self.screen.blit(image, (400 + X * 30, Y * 30))

    def clearCompleteLines(self, Y:int = 0):
        if Y == self.dimY:
            self.scoreTextRender = pg.font.Font(None, 30).render(f"Score: {self.score}", True, (255, 255, 255))
            return

        completeLine = True

        for X in range(self.dimX):
            if self.board[Y, X][0] == 0:
                completeLine = False

        if completeLine:
            self.score += np.sum(self.board[Y][:, 0]) * 100
            self.board[Y] = np.full([self.dimX, 4], [0, 0, 0, 0])
            self.board[3:Y+1] = np.roll(self.board[3:Y+1], shift=1, axis=0)

        self.score

        self.clearCompleteLines(Y + 1)

    def backEnd(self, deltaTime:int):
        if self.tickKey > 100 and self.move != [0,0]: 
            self.tickKey = 0
            self.pieceInGame[0].move(self.board,self.move)

        if self.tickPiece > 350:
            self.tickPiece = 0
            if self.pieceInGame[0].static: 
                self.checkModePieza()
                if (self.pieceInGame[0].y <= 3):
                    self.gameOver()
                self.pieceInGame.pop(0)
                self.pieceInGame.append(copy(choice(self.pieces)))
                
                self.clearCompleteLines()
    
            self.pieceInGame[0].move(self.board,[0,1])
    
        self.tickPiece += 1 * deltaTime
        self.tickKey += 1 * deltaTime
    
    def bucle(self):
        currentTime = pg.time.get_ticks()
        deltaTime = currentTime - self.lastTime
        self.lastTime = currentTime
        self.checkModeTiempo()

        if not self.isLoad:
            self.isLoad = True
            self.resetGame()

        self.drawBackground()
        self.drawPieces()
        self.drawUI()
        self.drawText()
        self.backEnd(deltaTime)
        self.events()