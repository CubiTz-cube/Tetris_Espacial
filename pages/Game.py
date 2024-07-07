import pygame as pg
import numpy as np

import library.piece as piece
from library.starsBack import StartMaker
from library.dynamicObjects import DynamicText, DynamicRect, DynamicImage
import public.images.loadImages as img
from library.starsBack import StartMaker
import library.dataFormating as df
import globalVariables as gv
from public.sonds.loadSonds import sfx
from library.imageEdit import convertImgToBn

from random import choice, randint
from copy import copy

class Game():
    def __init__(self):
        self.board = np.full([gv.dimY,gv.dimX], 0)
        self.pieces = []
        for index,active in enumerate(gv.activePieces):
            if active:
                self.pieces.append(piece.allPieces[index])

        self.piecesImg = {pieza.value:pieza.image for pieza in self.pieces}
        self.completepiecesImg = {
            1:img.completePieces["orangeBlack"],
            2:img.completePieces["orangeBlack"],
            3:img.completePieces["greenBlue"],
            4:img.completePieces["red"],
            5:img.completePieces["orange"],
            6:img.completePieces["greenBlue"],
            7:img.completePieces["yellow"],
            8:img.completePieces["green"],
            9:img.completePieces["green"],
            10:img.completePieces["blue"],
            11:img.completePieces["purple"],
            12:img.completePieces["blueBlack"],
        }

        self.lastTime = pg.time.get_ticks()
        self.screen = pg.display.get_surface()
        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]
        self.isLoad = False
        self.start_time = pg.time.get_ticks()
 
        self.pieceInGame:list[piece.Piece] = []
        self.pieceSaved:piece.Piece = None
        self.isPieceSavedNow = False
        self.score = 0
        self.tickPiece = 0
        self.speed = gv.speed
        self.limit = gv.limit

        self.tickKey = 0
        self.tickKeyWait = 0
        self.move = [0,0]
        self.moveDown = [0,0]
        self.PressLeft = False
        self.PressRight = False

        self.TIMEREVENT = pg.USEREVENT + 2
        pg.time.set_timer(self.TIMEREVENT, 1000)

        self.imgSavedPiece = DynamicImage(320, 80, 0.45, img.completePiecesNum["1"])
        self.textNextSavedPiece = DynamicText(310, 65, "Guardada", gv.fontAldrich, 20, "#FFFFFF")

        self.nextPiecesRender:list[DynamicImage] = []

        self.textRenderModeInactive = pg.font.Font(gv.fontLekton, 25).render(f"Sin modo", True, (255,255,255))
        self.textRenderModeTime = pg.font.Font(gv.fontLekton, 25).render(f"Tiempo:", True, (255,255,255))
        self.textRenderModePiece = pg.font.Font(gv.fontLekton, 25).render(f"Piezas:", True, (255,255,255))
        self.scoreTextRender = pg.font.Font(gv.fontLektonBold, 25).render(f"Score: {self.score}", True, (255,255,255))
        self.textRenderLimit = pg.font.Font(gv.fontLekton, 25).render(f"{self.limit}", True, (255,255,255))
        self.textNextPieces = DynamicText(886, 65, "Siguiente", gv.fontAldrich, 20, "#FFFFFF")
        self.textEscapeTo = DynamicText(540, 10, "Presiona ESC para Terminar el juego", gv.fontLekton, 15, "#FFFFFF")

        for i in range(4):
            self.nextPiecesRender.append(DynamicImage(900, 90+ ((50/720)*pg.display.Info().current_w)*i, 0.3, img.completePiecesNum["1"]))

        self.odsnumber = randint(1,17)
        self.starts = StartMaker(100, 10, minSpeed = 0.25, maxSpeed = 0.75)

        if gv.activeSond:
            self.sondPlace1 = pg.mixer.Sound(sfx["place1"])
            self.sondPlace2 = pg.mixer.Sound(sfx["place2"])
            self.sondPlace3 = pg.mixer.Sound(sfx["place3"])
            self.sondCompleteLine = pg.mixer.Sound(sfx["completeLine"])
            self.sondSwitch = pg.mixer.Sound(sfx["switch"])

    def resize(self):
        for index, obj in enumerate(self.nextPiecesRender):
            obj.changeCoord(None, 80+ ((50/720)*pg.display.Info().current_w)*index)
            obj.resize()
        self.starts.resize()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                gv.running = False
            if event.type == pg.VIDEORESIZE:
                self.resize()
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_a: 
                    self.PressLeft = False
                if event.key == pg.K_RIGHT or event.key == pg.K_d: 
                    self.PressRight = False
                if not self.PressLeft and not self.PressRight:
                    self.move = [0,0]
                if event.key == pg.K_DOWN or event.key == pg.K_s: 
                    self.moveDown = [0,0]
            if event.type == self.TIMEREVENT:
                if gv.mode == 1:
                    self.limit -= 1
                    self.textRenderLimit = pg.font.Font(gv.fontLekton, 25).render(f"{self.limit}", True, (255,255,255))
                    if self.limit <= 0: self.gameOver()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.pieceInGame[0].move(self.board,[-1,0])
                    self.move = [-1,0]
                    self.tickKey = 0
                    self.tickKeyWait = 0
                    self.PressLeft = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.pieceInGame[0].move(self.board,[1,0])
                    self.move = [1,0]
                    self.tickKey = 0
                    self.tickKeyWait = 0
                    self.PressRight = True
                if event.key == pg.K_SPACE:
                    while not self.pieceInGame[0].static:
                        self.pieceInGame[0].move(self.board,[0,1])
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.pieceInGame[0].move(self.board,[0,1])
                    self.moveDown = [0,1]
                    self.tickKey = 0
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.pieceInGame[0].rotateR(self.board)
                if event.key == pg.K_z:
                    self.pieceInGame[0].rotateR(self.board, False)
                if event.key == pg.K_x:
                    self.pieceInGame[0].rotateR(self.board)
                if event.key == pg.K_ESCAPE:
                    self.isLoad = False
                    self.gameOver()
                if event.key == pg.K_TAB and not self.isPieceSavedNow:
                    if gv.activeSond: pg.mixer.Sound.play(self.sondSwitch)
                    self.pieceInGame[0].erase(self.board)
                    pieceToSave = self.pieceInGame.pop(0)
                    pieceToSave.reset()
                    pieceToSave.x = int((self.dimX - pieceToSave.shape.shape[1]) / 2)
                    if self.pieceSaved != None: 
                        self.pieceInGame.insert(0, self.pieceSaved)
                    else:
                        self.pieceInGame.append(copy(choice(self.pieces)))
                    self.pieceSaved = pieceToSave
                    self.updateNextPieces()
                    if gv.piecesHasNum: self.imgSavedPiece.changeImg(convertImgToBn(img.completePiecesNum[str(self.pieceSaved.value)]))
                    else: self.imgSavedPiece.changeImg(convertImgToBn(self.completepiecesImg[self.pieceSaved.value]))
                    self.isPieceSavedNow = True

    def updateNextPieces(self):
        for index, nextPiece in enumerate(self.pieceInGame[1:]):
            if gv.piecesHasNum: self.nextPiecesRender[index].changeImg(img.completePiecesNum[str(nextPiece.value)])
            else: self.nextPiecesRender[index].changeImg(self.completepiecesImg[nextPiece.value])

    def resetGame(self):
        self.board = np.full([gv.dimY,gv.dimX,4], [0, 0, 0, 0])
        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]
        self.score = 0
        self.speed = gv.speed
        self.limit = gv.limit

        self.tickPiece = 0
        self.tickKey = 0
        self.move = [0,0]
        self.moveDown = [0,0]
        self.PressLeft = False
        self.PressRight = False

        self.pieces = []
        for index,active in enumerate(gv.activePieces): 
            if active:
                self.pieces.append(piece.allPieces[index])

        self.pieceInGame = []
        for i in range(5):
            pieceToAdd:piece.Piece = copy(choice(self.pieces))
            pieceToAdd.x = int((self.dimX - pieceToAdd.shape.shape[1]) / 2)
            self.pieceInGame.append(pieceToAdd)
        self.pieceSaved = None
        self.textRenderLimit = pg.font.Font(gv.fontLekton, 25).render(f"{self.limit}", True, (255,255,255))
        self.updateNextPieces()
        
    def checkModePieza(self):
        if gv.mode == 2:
            self.limit -= 1
            self.textRenderLimit = pg.font.Font(gv.fontLekton, 25).render(f"{self.limit}", True, (255,255,255))
            if self.limit <= 0: self.gameOver()
    
    def checkModeTiempo(self):
        pg.time.set_timer(pg.USEREVENT, 1000)
        if gv.mode == 1:
            self.textRenderLimit = pg.font.Font(gv.fontLekton, 25).render(f"{self.limit}", True, (255,255,255))

    def gameOver(self):
        if self.score > 0: df.addUserScore(gv.actualUser[0],self.score)
        gv.viewScore = self.score
        self.isLoad = False
        gv.actualPage = 7

    def drawGame(self):
        W,H = self.screen.get_size()
        BackX = (450/1280) * W
        BackY = (60/720) * H
        scale = ((390/1280) * W)/self.dimX 

        #Fondo del tablero
        pg.draw.rect(self.screen, "#050611", (BackX, BackY, scale*self.dimX+4, scale*(self.dimY-3)))

        #Lineas del fondo
        for Y in range(self.dimY-3):
            pg.draw.line(self.screen, "#141517", (BackX, Y*scale + BackY), (BackX + scale*self.dimX, Y*scale + BackY), 1)
            for X in range(self.dimX):
                pg.draw.line(self.screen, "#141517", (X*scale + BackX, BackY), (X*scale + BackX, scale*(self.dimY-3) + BackY), 1)

        #Cuadro del juego principal
        pg.draw.rect(self.screen, "#FFFFFF", (BackX-4, BackY-4,  scale*self.dimX+10, scale*(self.dimY-3)+10), 4)

        
        #Cuadro de la proximas piezas
        coordX = (BackX + (410/1280)*W)-4
        self.textNextPieces.render()
        pg.draw.rect(self.screen, "#FFFFFF", (coordX, BackY-4,  (150/1280)*W, (scale*(self.dimY-3)+10)*2/3), 4)

        #Cuadro del score y las ods
        pg.draw.rect(self.screen, "#FFFFFF", (coordX, BackY-4+(scale*(self.dimY-3)+10)*2/3 + 10,  (150/1280)*W, (scale*(self.dimY-3)+10)/3 - 10), 4)

        odsImg = img.ods[str(self.odsnumber)]
        scaleOds = int((80/1280)*W)
        odsImg = pg.transform.smoothscale(odsImg, (scaleOds, scaleOds))
        self.screen.blit(odsImg, (BackX + (410/1280)*W+(30/1280)*W, BackY-4+(scale*(self.dimY-3)+10)*2/3+(100/1280)*W))

        coordX = (BackX + (415/1280)*W)-4
        coordY = (scale*(self.dimY-3)+120)*2/3 + 10

        self.screen.blit(self.scoreTextRender, (coordX, coordY))
        coordY = (scale*(self.dimY-3)+180)*2/3 + 10
        if gv.mode == 0: self.screen.blit(self.textRenderModeInactive, (coordX, coordY))
        elif gv.mode == 1: self.screen.blit(self.textRenderModeTime, (coordX, coordY))  
        else: self.screen.blit(self.textRenderModePiece, (coordX, coordY))
        if  gv.mode != 0: self.screen.blit(self.textRenderLimit, ((BackX + (520/1280)*W)-4, coordY))

        #Cuadro de la pieza guardada
        pg.draw.rect(self.screen, "#FFFFFF", ((BackX - (10/1280)*W)-4-(150/1280)*W, BackY-4,  (150/1280)*W, (scale*(self.dimY-3)+10)/4), 4)
        self.textNextSavedPiece.render()
        if self.pieceSaved != None:
            self.imgSavedPiece.render()

        #Piezas
        for Y in range(3, self.dimY):
            for X in range(self.dimX):
                pieceX = X * scale + BackX
                pieceY = (Y-3) * scale + BackY
                if self.board[Y,X][0] != 0:
                    if gv.piecesHasNum: image = img.piecesNum[str(self.board[Y,X][0])]
                    else: image = self.piecesImg[self.board[Y,X][0]]
                    image = pg.transform.scale(image, (scale+1,scale+1))
                    self.screen.blit(image, (pieceX, pieceY))
                if self.board[Y,X][0] == 0 and X >= self.pieceInGame[0].x + self.pieceInGame[0].startEndPieceShape()[0] and X < self.pieceInGame[0].x + self.pieceInGame[0].startEndPieceShape()[1]:
                    pg.draw.rect(self.screen, "#090B1F", (pieceX, pieceY, scale+1, scale+1))

    def drawPieces(self):
        for nextPiece in self.nextPiecesRender:
            nextPiece.render()

    def clearCompleteLines(self, Y:int = 0):
        if Y == self.dimY:
            self.scoreTextRender = pg.font.Font(gv.fontLektonBold, 25).render(f"Score: {self.score}", True, (255, 255, 255))
            return

        completeLine = True

        for X in range(self.dimX):
            if self.board[Y, X][0] == 0:
                completeLine = False

        if completeLine:
            if gv.activeSond: pg.mixer.Sound.play(self.sondCompleteLine)
            self.score += np.sum(self.board[Y][:, 0]) * 100
            self.board[Y] = np.full([self.dimX, 4], [0, 0, 0, 0])
            self.board[3:Y+1] = np.roll(self.board[3:Y+1], shift=1, axis=0)

        self.score

        self.clearCompleteLines(Y + 1)

    def backEnd(self, deltaTime:int):
        if self.tickKey > 70 and (self.move != [0,0] or self.moveDown != [0,0]): 
            if self.tickKeyWait > 150: self.pieceInGame[0].move(self.board,self.move)
            self.pieceInGame[0].move(self.board,self.moveDown)
            self.tickKey = 0

        if self.tickPiece > 350:
            self.tickPiece = 0
            if self.pieceInGame[0].static: 
                if gv.activeSond: pg.mixer.Sound.play(choice([self.sondPlace1, self.sondPlace2, self.sondPlace3]))

                self.checkModePieza()
                if (self.pieceInGame[0].y <= 3):
                    self.gameOver()

                self.pieceInGame.pop(0)
                pieceToAdd:piece.Piece = copy(choice(self.pieces))
                pieceToAdd.x = int((self.dimX - pieceToAdd.shape.shape[1]) / 2)
                self.pieceInGame.append(pieceToAdd)

                self.updateNextPieces()
                self.isPieceSavedNow = False
                if self.pieceSaved != None: 
                    if gv.piecesHasNum: self.imgSavedPiece.changeImg(img.completePiecesNum[str(self.pieceSaved.value)])
                    else: self.imgSavedPiece.changeImg(self.completepiecesImg[self.pieceSaved.value])
                
                self.clearCompleteLines()
                self.odsnumber = randint(1,17)
                self.speed += 0.01
    
            if self.moveDown == [0,0]: self.pieceInGame[0].move(self.board,[0,1])
    
        self.tickPiece += (1 * deltaTime) * self.speed
        self.tickKey += 1 * deltaTime
        self.tickKeyWait += 1 * deltaTime
    
    def bucle(self):
        currentTime = pg.time.get_ticks()
        deltaTime = currentTime - self.lastTime
        self.lastTime = currentTime
        self.checkModeTiempo()

        if not self.isLoad:
            self.isLoad = True
            self.resetGame()

        self.screen.fill("#050611")
        self.textEscapeTo.render()
        self.starts.render()
        self.drawGame()
        self.drawPieces()
        self.backEnd(deltaTime)
        self.events()