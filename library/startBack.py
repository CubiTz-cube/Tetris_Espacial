import pygame as pg

class Start():
    def __init__(self, X, Y, scale) -> None:
        self.screen = pg.display.get_surface()

        self.X = X
        self.Y = Y
        self.scale = scale

    def draw(self):
        pg.draw.rect(self.screen, (255,255,255), (self.X, (self.Y-3), self.scale, self.scale))

    def move(self, x, y):
        self.X += x
        self.Y += y

class StartMaker():
    def __init__(self, speed) -> None:
        self.speed = speed

        self.starts = []
        self.screen = pg.display.get_surface()
        self.H = self.screen.get_height()
        self.W = self.screen.get_width()

    def addStart(self, X, Y, scale):
        self.starts.append(Start(X, Y, scale))

    def animateStarts(self):
        for start in self.starts:
            start.draw()
            start.move(0,self.speed)
            if start.Y > self.H:
                start.Y = 0
            
