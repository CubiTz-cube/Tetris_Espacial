import numpy as np
import pygame as pg
from random import choice
from copy import copy

from Piece import Piece
from shapes import *
from pages.Game import Game

N = 21
M = 12
board = np.zeros((N, M), dtype=int)

pieces = [Piece(board, shape_I, 1),Piece(board, shape_L, 3),Piece(board, shape_LI, 4),Piece(board, shape_D, 5), Piece(board, shape_O, 7, False), Piece(board, shape_T, 8)]

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-50), pg.RESIZABLE)
clock = pg.time.Clock()

gamePieces = []
inGame = [copy(choice(pieces)) for _ in range(2)]
time = 100
timeT = 0
move = [0,0]

pages = [Game(board, inGame)]
page = 0

while True:
    deltaTime = clock.tick(60) / 1000
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
                move = [-1,0]
                timeT = 0
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                inGame[0].move([1,0])
                move = [1,0]
                timeT = 0
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                while not inGame[0].static:
                    inGame[0].move([0,1])
            if event.key == pg.K_UP or event.key == pg.K_w:
                inGame[0].rotateR()
        if event.type == pg.KEYUP:
            move = [0,0]

    if timeT > int(540 * deltaTime) and move != [0,0]: 
        timeT = 0
        inGame[0].move(move)

    if time > int(1500 * deltaTime):
        time = 0
        if inGame[0].static: 
            gamePieces.append(inGame.pop(0))
            inGame.append(copy(choice(pieces)))

        #Cambiar por recursividad y mandar señal a interfaz cuando se compelta una fila
        for Y in range(3,N):
            completeLine = True
            for X in range(M):
                if board[Y,X] == 0:
                    completeLine = False

            if completeLine: 
                board[Y] = np.zeros(M, dtype=int)
                board[3:Y+1] = np.roll(board[3:Y+1], shift=1, axis=0)


        inGame[0].move([0,1])

    pages[page].bucle()
    time += 1
    timeT += 1
    pg.display.flip()