import numpy as np
import pygame as pg

from pages.Login import Login
from pages.Register import Register
from pages.Menu import Menu
from pages.Selection import Selection
from pages.Game import Game
from pages.Leaderboard import Leaderboard
from pages.Config import Config

#Reorganizar los saltos a paginas ya que cambie los indices de estas

try:
    open("./data/JUGADORES.bin", "x")
except:
    pass

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-50), pg.RESIZABLE)
clock = pg.time.Clock()

N = 21
M = 12
board = np.full([N,M,4], [0, 0, 0, 0])

page = 3
def changePage(newPage): global page; page = newPage
pages = [
    Login(changePage), # 0
    Register(changePage), # 1
    Menu(changePage), # 2
    Selection(changePage), # 3
    Game(changePage), # 4
    Leaderboard(changePage), # 5
    Config(changePage), # 6
]

while True:
    pages[page].bucle()
    clock.tick(60)
    pg.display.flip()