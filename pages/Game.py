import pygame as pg
import numpy as np
from Piece import Piece
from random import choice
from copy import copy

colors = [(50,50,50), (100, 100, 200), (200, 100, 100), (100, 200, 100), (200, 200, 100), (100, 100, 200), (200, 100, 200), (100, 200, 200), (200, 200, 200)]

class Game():
    def __init__(self, clock:pg.time.Clock, board:np.ndarray[any], pieces:list[Piece]):
        self.clock = clock
        self.screen = pg.display.get_surface()
        self.board = board
        self.pieces = pieces
        self.pieceInGame = [copy(choice(pieces)) for _ in range(2)]
        self.gamePieces = []

        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]

        self.time = 0
        self.timeT = 0
        self.move = [0,0]
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
                    self.pieceInGame[0].move([-1,0])
                    self.move = [-1,0]
                    self.timeT = 0
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.pieceInGame[0].move([1,0])
                    self.move = [1,0]
                    self.timeT = 0
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    while not self.pieceInGame[0].static:
                        self.pieceInGame[0].move([0,1])
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.pieceInGame[0].rotateR()
            if event.type == pg.KEYUP:
                self.move = [0,0]

    def frontEnd(self):
        self.screen.fill((0,0,0))

        pg.draw.rect(self.screen, (255,255,255), (0, 0, self.dimX *30, (self.dimY-3) * 30))

        for Y in range(3, self.dimY):
            for X in range(self.dimX):
                if self.board[Y,X] != 0:
                    pg.draw.rect(self.screen, colors[self.board[Y,X]], (X * 30, (Y-3) * 30, 30, 30))
                elif self.pieceInGame[0].x in [X,X-1,X-2]:
                    pg.draw.rect(self.screen, (240,240,240), (X * 30, (Y-3) * 30, 30, 30))

        for Y in range(3):
            for X in range(3):
                if self.pieceInGame[1].shape[Y,X] != 0:
                    pg.draw.rect(self.screen, colors[self.pieceInGame[1].value], (400 + X * 30, Y * 30, 30, 30))

    def backEnd(self):
        deltaTime = self.clock.tick(60) / 1000
        if self.timeT > int(540 * deltaTime) and self.move != [0,0]: 
            self.timeT = 0
            self.pieceInGame[0].move(self.move)

        if self.time > int(1500 * deltaTime):
            self.time = 0
            if self.pieceInGame[0].static: 
                self.gamePieces.append(self.pieceInGame.pop(0))
                self.pieceInGame.append(copy(choice(self.pieces)))

            #Cambiar por recursividad
            for Y in range(3,self.dimY):
                completeLine = True
                for X in range(self.dimX):
                    if self.board[Y,X] == 0:
                        completeLine = False

                if completeLine: 
                    self.board[Y] = np.zeros(self.dimX, dtype=int)
                    self.board[3:Y+1] = np.roll(self.board[3:Y+1], shift=1, axis=0)

            self.pieceInGame[0].move([0,1])

        self.time += 1
        self.timeT += 1

    def bucle(self):
        self.events()

        self.frontEnd()

        self.backEnd()
                    
