import pygame as pg
import numpy as np

class Game():
    def __init__(self, board:np.ndarray[any]):
        self.screen = pg.display.get_surface()
        self.board = board

        self.dimY = self.board.shape[0]
        self.dimX = self.board.shape[1]

    def bucle(self):
        screen = self.screen
        board = self.board
        screen.fill((0,0,0))

        for Y in range(self.dimY):
            for X in range(self.dimX):
                if board[Y,X] != 0:
                    pg.draw.rect(screen, (100, 100, 200), (X * 30, Y * 30, 30, 30))
                    
