import numpy as np
from random import choice
from time import sleep

colors = ["a"]

class Piece:
    def __init__(self, board:np.ndarray[any], shape:np.ndarray[any], value:int) -> None:
        self.board = board
        self.shape = shape
        self.value = value

        self.x = 0
        self.y = 0
        self.color = choice(colors)
        self.static = False

    def erase(self):
        for Y in range(3):
            for X in range(3):
                if self.shape[Y, X] == 1:
                    self.board[self.y + Y, self.x + X] = 0

    def create(self):
        for Y in range(3):
            for X in range(3):
                if self.shape[Y, X] == 1:
                    self.board[self.y + Y, self.x + X] = self.value

    def rotateR(self, right:bool = True):
        if self.static: return

        self.erase()
        if right: self.shape = np.rot90(self.shape, -1)
        else: self.shape = np.rot90(self.shape)
        self.create()

    def stop(self):
        self.static = True

    def move(self, x:int = 0, y:int = 0):
        if self.static: return

        if x == 0 and self._colisionY(): return
        elif y == 0 and self._colisionX(True if x > 0 else False): return

        self.erase()
        self.x += x
        self.y += y
        self.create()
    
    def _colisionX(self, right:bool = True):
        result = False
        for Y in range(3):
            for X in range(3):
                if self.shape[Y, X] == 1:
                    if right and X + 1 == self.shape.shape[1] or X + 1 < self.shape.shape[1] and self.shape[Y, X+1] != 1:
                        if self.x + X + 1 == self.board.shape[1] or self.board[self.y + Y, self.x + X + 1] != 0:
                            result = True
                    if not right and X - 1 == 0 or X - 1 < 0 and self.shape[Y, X-1] != 1:
                        if self.x + X - 1 == -1 or self.board[self.y + Y, self.x + X - 1] != 0:
                            result = True
        print(result)
        return result
    
    def _colisionY(self):
        for X in range(3):
            for Y in range(3):
                if self.shape[Y, X] == 1:
                    if Y + 1 == self.shape.shape[0] or Y + 1 < self.shape.shape[0] and self.shape[Y+1, X] != 1:
                        if self.y + Y +1 == self.board.shape[0] or self.board[self.y + Y + 1, self.x + X] != 0:
                            self.stop()
                            return True 