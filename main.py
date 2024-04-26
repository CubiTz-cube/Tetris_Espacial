import numpy as np
import pygame as pg
from random import choice
from copy import copy

from Piece import Piece
from pages.Game import Game

N = 15
M = 9
board = np.zeros((N, M), dtype=int)

shape_I = np.zeros((3, 3), dtype=int)
shape_I[0, 1] = 1
shape_I[1, 1] = 1
shape_I[2, 1] = 1

shape_L = np.zeros((3, 3), dtype=int)
shape_L[0, 1] = 1
shape_L[1, 1] = 1
shape_L[2, 1] = 1
shape_L[2, 2] = 1

shape_LI = np.zeros((3, 3), dtype=int)
shape_LI[0, 1] = 1
shape_LI[1, 1] = 1
shape_LI[2, 1] = 1
shape_LI[2, 0] = 1

shape_D = np.zeros((3, 3), dtype=int)
shape_D[1, 0] = 1
shape_D[1, 1] = 1
shape_D[2, 1] = 1
shape_D[2, 2] = 1

shape_O = np.zeros((3, 3), dtype=int)
shape_O[0, 0] = 1
shape_O[1, 0] = 1
shape_O[0, 1] = 1
shape_O[1, 1] = 1

shape_T = np.zeros((3, 3), dtype=int)
shape_T[0, 0] = 1
shape_T[0, 1] = 1
shape_T[0, 2] = 1
shape_T[1, 1] = 1
shape_T[2, 1] = 1

pieces = [Piece(board, shape_I, 1),Piece(board, shape_L, 3),Piece(board, shape_LI, 4),Piece(board, shape_D, 5), Piece(board, shape_O, 7, False), Piece(board, shape_T, 9)]

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-1000, H-500), pg.RESIZABLE)

gamePieces = []
inGame = [copy(choice(pieces)) for _ in range(2)]
time = 0

pages = [Game(board)]

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.VIDEORESIZE:
            #Reside screen
            pass
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                inGame[0].move([-1,0])
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                inGame[0].move([1,0])
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                inGame[0].move([0,1])
            if event.key == pg.K_UP or event.key == pg.K_w:
                inGame[0].rotateR()
        if event.type == pg.KEYUP:
            move = [0,0]

    if time > 50:
        time = 0
        if inGame[0].static: 
            gamePieces.append(inGame.pop(0))
            inGame.append(copy(choice(pieces)))

        inGame[0].move([0,1])

    pages[0].bucle()
    time += 1
    pg.display.flip()
    pg.time.Clock().tick(60)