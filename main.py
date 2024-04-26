import numpy as np
import pygame as pg

from pages.Game import Game

N = 21
M = 12
board = np.zeros((N, M), dtype=int)

pg.init()
W = pg.display.Info().current_w
H = pg.display.Info().current_h
pg.display.set_mode((W-100, H-50), pg.RESIZABLE)
clock = pg.time.Clock()

pages = [Game(clock,board)]
page = 0

while True:
    pages[page].bucle()
    
    pg.display.flip()