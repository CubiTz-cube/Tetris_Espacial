import pygame as pg
import numpy as np

from library.piece import *
import public.images.loadImages as img
from library.startBack import StartMaker
import globalVariables as gv

from random import choice
from copy import copy

piezaIvar = Piece(shape_I, 1 , img.pieceOrangeRed)
piezaI = Piece(shape_I, 2, img.pieceRed)
piezaL = Piece(shape_L, 3, img.pieceGreen)
piezaLI = Piece(shape_LI, 4, img.pieceRed)
piezaSI = Piece(shape_SI, 5, img.pieceOrange)
piezaLvar = Piece(shape_L, 6, img.pieceGreen)
piezaO = Piece(shape_O, 7, img.pieceYellow, False)
piezaT = Piece(shape_T, 8, img.pieceGreenBlue)
piezaTvar = Piece(shape_T, 9, img.pieceGreenBlue)
piezaS = Piece(shape_S, 10, img.pieceBlue)
piezaTmin = Piece(shape_Tmin, 11, img.piecePurple)
piezaImax = Piece(shape_Imax, 12, img.piecePink)

class Game():
    def __init__(self):
        self.board = np.full([gv.dimY,gv.dimX], 0)
        self.allPieces = [piezaIvar, piezaI, piezaL, piezaLI, piezaS, piezaLvar, piezaO, piezaT, piezaTvar, piezaS, piezaTmin, piezaImax]
        self.pieces = []
        for index,active in enumerate(gv.activePieces):
            if active:
                self.pieces.append(self.allPieces[index])
        #[piezaIvar, piezaI, piezaL, piezaLI, piezaS, piezaLvar, piezaO, piezaT, piezaTvar] piezas que pode franklin
        #[piezaImax, piezaTmin, piezaO, piezaS, piezaSI, piezaL, piezaLI] Piezas clasicas de tetris
        self.piecesImg = {pieza.value:pieza.image for pieza in self.pieces}

        self.lastTime = pg.time.get_ticks()
        self.screen = pg.display.get_surface()
        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]
        self.isLoad = False

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
                self.pieces.append(self.allPieces[index])
        self.pieceInGame = [copy(choice(self.pieces)) for _ in range(2)]

    def checkMode(self):
        if gv.limit <= 0: self.gameOver()
        #Juan david separa esto en dos partes y usa solo la varialbes limit
        if gv.mode == 1:
            gv.limit -= 1
        elif gv.mode == 2:  
            gv.limit -=1
            if gv.limit <= 0:
                self.gameOver()
              
    def gameOver(self):
        #self.gameOverScene = True
        exit()

    def drawBackground(self):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen, (255,255,255), (0, 0, self.dimX *30, (self.dimY-3) * 30))

    def drawText(self):
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

    def clearCompleteLines(self, Y = 0, score = 0):
        if Y >= self.dimY:
            self.score =  score * 100
            self.scoreTextRender = pg.font.Font(None, 30).render(f"Score: {self.score}", True, (255,255,255))
            return

        completeLine = True
        if completeLine:
            for X in range(self.dimX):
                if self.board[Y,X][0] == 0:
                    completeLine = False

        if completeLine:
            score += (self.board[Y][X][0])
            self.board[Y] = np.full([self.dimX,4], [0,0,0,0])
            self.board[3:Y+1] = np.roll(self.board[3:Y+1], shift=1, axis=0)

        self.clearCompleteLines(Y+1, score)
                
    def backEnd(self, deltaTime:int):
        #self.checkMode() se cierra el juego
        if self.tickKey > 100 and self.move != [0,0]: 
            self.tickKey = 0
            self.pieceInGame[0].move(self.board,self.move)

        if self.tickPiece > 350:
            self.tickPiece = 0
            if self.pieceInGame[0].static: 
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

        if not self.isLoad:
            self.isLoad = True
            self.resetGame()

        self.drawBackground()
        self.drawPieces()
        self.drawUI()
        self.drawText()
        self.backEnd(deltaTime)
        self.events()