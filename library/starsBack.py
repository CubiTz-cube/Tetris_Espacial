import pygame as pg
import random as rd

class Start():
    def __init__(self, X, Y, scale, speed) -> None:
        self.screen = pg.display.get_surface()

        self.X = X
        self.Y = Y
        self.Z = 0.1 + rd.random() * (1 - 0.1)
        self.scale = scale
        self.speed = speed

    def draw(self):
        pg.draw.rect(self.screen, (255,255,255), (self.X, (self.Y-3), self.scale*self.Z, self.scale*self.Z))

    def move(self, x, y):
        self.X += x
        self.Y += y

class StartMaker():
    def __init__(self, num, size, minSpeed, maxSpeed) -> None:
        self.num = num
        self.size = size
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed

        self.starts = []
        self.screen = pg.display.get_surface()
        self.H = self.screen.get_height()
        self.W = self.screen.get_width()

        self.generateStarts()

    def resize(self):
        self.H = self.screen.get_height()
        self.W = self.screen.get_width()
        self.starts = []
        self.generateStarts()

    def _addStart(self, X, Y, scale, speed):
        self.starts.append(Start(X, Y, scale, speed))

    def generateStarts(self):
        for i in range(0, self.num):
            self._addStart(rd.random()*self.W, rd.random()*self.H, self.size,  self.minSpeed + rd.random() * (self.maxSpeed - self.minSpeed))

    def render(self):
        for start in self.starts:
            start.draw()
            start.move(0,start.speed)
            if start.Y > self.H:
                start.Y = 0
            
