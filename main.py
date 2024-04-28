import numpy as np
import pygame as pg

from Piece import *
from pages.Register import Register
from pages.Menu import Menu
from pages.Leaderboard import Leaderboard
from pages.Selection import Selection
from pages.Game import Game

N = 21
M = 12
board = np.full([N,M,4], [0, 0, 0, 0])

piI = Piece(board, shape_I, 1)
piL = Piece(board, shape_L, 3)
piLI = Piece(board, shape_LI, 4)
piD = Piece(board, shape_D, 5)
piO = Piece(board, shape_O, 7, False)
piT = Piece(board, shape_T, 8)

try:
    open("./data/JUGADORES.bin", "x")
except:
    pass

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-50), pg.RESIZABLE)
clock = pg.time.Clock()

pieces:list[Piece] = [piI, piL, piLI, piD, piO, piT]
mode = 0

page = 3
def changePage(newPage):
    global page
    page = newPage

pages = [
    Register(changePage),
    Menu(changePage),
    Leaderboard(changePage),
    Selection(changePage),
    Game(changePage,board, pieces, mode)
]

while True:
    pages[page].bucle()
    
    pg.display.flip()