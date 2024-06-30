import numpy as np
import pygame as pg

import globalVariables as gv
import public.sonds.loadSonds as sonds

from pages.Login import Login
from pages.Register import Register
from pages.Menu import Menu
from pages.Selection import Selection
from pages.Game import Game
from pages.Leaderboard import Leaderboard
from pages.Config import Config
from pages.GameOver import GameOver

try:
    open("./data/JUGADORES.bin", "x")
except:
    pass

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-100), pg.RESIZABLE)
clock = pg.time.Clock()

try:
    pg.mixer.init()
    gv.activeSond = True
except:
    gv.activeSond = False


sonds.playMusic(sonds.music["menu"])

pages = [
    Login(),
    Register(),
    Menu(),
    Selection(),
    Game(),
    Leaderboard(),
    Config(),
    GameOver()
]

while True:
    pages[gv.actualPage].bucle()
    clock.tick(60)
    pg.display.flip()