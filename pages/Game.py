import pygame as pg
import numpy as np
from Piece import Piece

colors = [(50,50,50), (100, 100, 200), (200, 100, 100), (100, 200, 100), (200, 200, 100), (100, 100, 200), (200, 100, 200), (100, 200, 200), (200, 200, 200)]

class Game():
    def __init__(self, board:np.ndarray[any], pieceList:list[Piece]):
        self.screen = pg.display.get_surface()
        self.board = board
        self.pieceList = pieceList

        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]

    def bucle(self):
        screen = self.screen
        board = self.board
        screen.fill((0,0,0))

        pg.draw.rect(screen, (255,255,255), (0, 0, self.dimX *30, (self.dimY-3) * 30))

        for Y in range(3, self.dimY):
            for X in range(self.dimX):
                if board[Y,X] != 0:
                    pg.draw.rect(screen, colors[board[Y,X]], (X * 30, (Y-3) * 30, 30, 30))
                elif self.pieceList[0].x in [X,X-1,X-2]:
                    pg.draw.rect(screen, (240,240,240), (X * 30, (Y-3) * 30, 30, 30))

        for Y in range(3):
            for X in range(3):
                if self.pieceList[1].shape[Y,X] != 0:
                    pg.draw.rect(screen, colors[self.pieceList[1].value], (400 + X * 30, Y * 30, 30, 30))
                    
