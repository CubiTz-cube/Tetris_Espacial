import numpy as np
from random import choice
from time import sleep

colors = [(100, 100, 200), (200, 100, 100), (100, 200, 100), (200, 200, 100), (100, 100, 200), (200, 100, 200), (100, 200, 200)]

shape_I = np.zeros((3, 3), dtype=int)
shape_I[0, 1] = 1
shape_I[1, 1] = 1
shape_I[2, 1] = 1

shape_L = np.zeros((3, 3), dtype=int)
shape_L[0, 1] = 1
shape_L[1, 1] = 1
shape_L[2, 1] = 1
shape_L[2, 2] = 1

shape_LI = np.zeros((3, 3), dtype=int)
shape_LI[0, 1] = 1
shape_LI[1, 1] = 1
shape_LI[2, 1] = 1
shape_LI[2, 0] = 1

shape_S = np.zeros((3, 3), dtype=int)
shape_S[1, 0] = 1
shape_S[1, 1] = 1
shape_S[2, 1] = 1
shape_S[2, 2] = 1

shape_SI = np.zeros((3, 3), dtype=int)
shape_SI[2, 0] = 1
shape_SI[2, 1] = 1
shape_SI[1, 1] = 1
shape_SI[1, 2] = 1

shape_O = np.zeros((3, 3), dtype=int)
shape_O[0, 0] = 1
shape_O[1, 0] = 1
shape_O[0, 1] = 1
shape_O[1, 1] = 1

shape_T = np.zeros((3, 3), dtype=int)
shape_T[0, 0] = 1
shape_T[0, 1] = 1
shape_T[0, 2] = 1
shape_T[1, 1] = 1
shape_T[2, 1] = 1

shape_Tmin = np.zeros((3, 3), dtype=int)
shape_Tmin[1, 0] = 1
shape_Tmin[1, 1] = 1
shape_Tmin[1, 2] = 1
shape_Tmin[2, 1] = 1

shape_Imax = np.zeros((4, 4), dtype=int)
shape_Imax[0, 1] = 1
shape_Imax[1, 1] = 1
shape_Imax[2, 1] = 1
shape_Imax[3, 1] = 1

class Piece:
    def __init__(self, board:np.ndarray[any], shape:np.ndarray[any], value:int, rotate = True) -> None:
        self.board = board
        self.shape = shape
        self.value = value
        self.rotate = rotate

        self.x = 0
        self.y = 0
        self.color = choice(colors)
        self.static = False

    def erase(self):
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    self.board[self.y + Y, self.x + X] = 0

    def create(self):
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    self.board[self.y + Y, self.x + X][0] = self.value
                    self.board[self.y + Y, self.x + X][1] = self.color[0]
                    self.board[self.y + Y, self.x + X][2] = self.color[1]
                    self.board[self.y + Y, self.x + X][3] = self.color[2]

    def rotateR(self, right:bool = True):
        if self.static or not self.rotate: return


        self.erase()
        if right: 
            tempShape = np.rot90(self.shape, -1)
            if not self._colisionR(tempShape): self.shape = tempShape

        else:
            tempShape = np.rot90(self.shape)
            if not self._colisionR(tempShape): self.shape = tempShape
        self.create()

    def stop(self):
        self.static = True

    def move(self, coords:tuple[int, int]):
        if self.static: return
        x, y = coords

        if x == 0 and self._colisionY(): return
        elif y == 0 and self._colisionX(True if x > 0 else False): return

        self.erase()
        self.x += x
        self.y += y
        self.create()
    
    def _colisionX(self, right:bool = True):
        result = False
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    if right and (X + 1 == self.shape.shape[1] or (X + 1 < self.shape.shape[1] and self.shape[Y, X+1] != 1)):
                        if self.x + X + 1 == self.board.shape[1] or self.board[self.y + Y, self.x + X + 1][0] != 0:
                            result = True
                    elif not right and (X - 1 == -1 or (X - 1 >= 0 and self.shape[Y, X-1] != 1)):
                        if self.x + X - 1 == -1 or self.board[self.y + Y, self.x + X - 1][0] != 0:
                            result = True
        return result
    
    def _colisionY(self):
        for X in range(self.shape.shape[1]):
            for Y in range(self.shape.shape[0]):
                if self.shape[Y, X] == 1:
                    if Y + 1 == self.shape.shape[0] or Y + 1 < self.shape.shape[0] and self.shape[Y+1, X] != 1:
                        if self.y + Y +1 == self.board.shape[0] or self.board[self.y + Y + 1, self.x + X][0] != 0:
                            self.stop()
                            return True
    
    def _colisionR(self, tempShape):
        for Y in range(self.shape.shape[0]):
                for X in range(self.shape.shape[1]):
                    if tempShape[Y, X] == 1:
                        if self.x + X < 0 or self.x + X >= self.board.shape[1] or self.board[self.y + Y, self.x + X][0] != 0:
                            return True
        return False
