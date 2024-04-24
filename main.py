import numpy as np
import pygame as pg
from random import choice

from piece import Piece

N = 21
M = 12
board = np.zeros((N, M), dtype=int)

shape_L = np.zeros((3, 3), dtype=int)
shape_L[0, 1] = 1
shape_L[1, 1] = 1
shape_L[2, 1] = 1
shape_L[2, 2] = 1
piece_L = Piece(board, shape_L, 1)
shape_O = np.zeros((3, 3), dtype=int)
shape_O[0, 0] = 1
shape_O[1, 0] = 1
shape_O[0, 1] = 1
shape_O[1, 1] = 1
piece_O = Piece(board, shape_O, 2)

pieces = [piece_L]

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-1000, H-500), pg.RESIZABLE)

gamePieces = []
inGame = [choice(pieces) for _ in range(2)]
time = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.VIDEORESIZE:
            #Reside screen
            pass
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                inGame[0].move(-1, 0)
            if event.key == pg.K_RIGHT:
                inGame[0].move(1, 0)
            if event.key == pg.K_DOWN:
                inGame[0].move(0, 1)
            if event.key == pg.K_UP:
                inGame[0].rotateR()

    if time > 50:
        time = 0
        if inGame[0].static: 

        print(board)
        inGame[0].move(0, 1)
        
    
    time += 1
    pg.display.flip()
    pg.time.Clock().tick(60)