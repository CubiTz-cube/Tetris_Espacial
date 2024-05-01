import numpy as np
import pygame as pg

from piece import *
from pages.Login import Login
from pages.Register import Register
from pages.Menu import Menu
from pages.Leaderboard import Leaderboard
from pages.Selection import Selection
from pages.Game import Game

N = 21
M = 12
board = np.full([N,M,4], [0, 0, 0, 0])

piezaIvar = Piece(board, shape_I, 1)
piezaI = Piece(board, shape_I, 2)
piezaL = Piece(board, shape_L, 3)
piezaLI = Piece(board, shape_LI, 4)
piezaS = Piece(board, shape_S, 5)
piezaLvar = Piece(board, shape_L, 6)
piezaO = Piece(board, shape_O, 7, False)
piezaT = Piece(board, shape_T, 8)
piezaTvar = Piece(board, shape_T, 9)
piezaSI = Piece(board, shape_SI, 10)
piezaTmin = Piece(board, shape_Tmin, 11)
piezaImax = Piece(board, shape_Imax, 12)

try:
    open("./data/JUGADORES.bin", "x")
except:
    pass

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-50), pg.RESIZABLE)
clock = pg.time.Clock()

pieces:list[Piece] = [piezaImax, piezaTmin, piezaO, piezaS, piezaSI, piezaL, piezaLI]#[piezaIvar, piezaI, piezaL, piezaLI, piezaS, piezaLvar, piezaO, piezaT, piezaTvar]
mode = 1
limit = 3

page = 5
def changePage(newPage):
    global page
    page = newPage

pages = [
    Login(changePage),
    Register(changePage),
    Menu(changePage),
    Leaderboard(changePage),
    Selection(changePage),
    Game(changePage,board, pieces, mode, limit)
]

while True:
    pages[page].bucle()
    pg.display.flip()