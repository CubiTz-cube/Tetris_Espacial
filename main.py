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

pages = [Game(clock,board, pieces)]
page = 0

while True:
    pages[page].bucle()
    
    pg.display.flip()