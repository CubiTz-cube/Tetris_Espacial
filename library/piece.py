import numpy as np
import globalVariables as gv
import public.images.loadImages as img

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
shape_Tmin[0, 1] = 1

shape_Imax = np.zeros((4, 4), dtype=int)
shape_Imax[0, 1] = 1
shape_Imax[1, 1] = 1
shape_Imax[2, 1] = 1
shape_Imax[3, 1] = 1

class Piece:
    def __init__(self, shape:np.ndarray[any], value:int, image, rotate = True) -> None:
        self.shape = shape
        self.value = value
        self.canRotate = rotate

        self.x = 0
        self.y = 0
        self.static = False

        self.image = image

    def reset(self):
        self.x = 0
        self.y = 0
        self.static = False

    def erase(self, board:np.ndarray[any]):
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    board[self.y + Y, self.x + X] = 0

    def create(self, board:np.ndarray[any]):
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    board[self.y + Y, self.x + X] = self.value

    def rotateR(self,board:np.ndarray[any], right:bool = True):
        if self.static or not self.canRotate: return


        self.erase(board)
        if right: 
            tempShape = np.rot90(self.shape, -1)
            if not self._colisionR(board,tempShape): self.shape = tempShape

        else:
            tempShape = np.rot90(self.shape)
            if not self._colisionR(board,tempShape): self.shape = tempShape
        self.create(board)

    def stop(self):
        self.static = True

    def move(self, board:np.ndarray[any], coords:tuple[int, int]):
        if self.static: return
        x, y = coords

        if x == 0 and self._colisionY(board): return
        elif y == 0 and self._colisionX(board,True if x > 0 else False): return

        self.erase(board)
        self.x += x
        self.y += y
        self.create(board)

    def startEndPieceShape(self):
        number = []
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y,X] == 1:
                    number.append(X)
        return min(number), max(number)+1

    def _colisionX(self,board:np.ndarray[any], right:bool = True):
        result = False
        for Y in range(self.shape.shape[0]):
            for X in range(self.shape.shape[1]):
                if self.shape[Y, X] == 1:
                    if right and (X + 1 == self.shape.shape[1] or (X + 1 < self.shape.shape[1] and self.shape[Y, X+1] != 1)):
                        if self.x + X + 1 == board.shape[1] or board[self.y + Y, self.x + X + 1][0] != 0:
                            result = True
                    elif not right and (X - 1 == -1 or (X - 1 >= 0 and self.shape[Y, X-1] != 1)):
                        if self.x + X - 1 == -1 or board[self.y + Y, self.x + X - 1][0] != 0:
                            result = True
        return result
    
    def _colisionY(self, board:np.ndarray[any]):
        for X in range(self.shape.shape[1]):
            for Y in range(self.shape.shape[0]):
                if self.shape[Y, X] == 1:
                    if Y + 1 == self.shape.shape[0] or Y + 1 < self.shape.shape[0] and self.shape[Y+1, X] != 1:
                        if self.y + Y +1 == board.shape[0] or board[self.y + Y + 1, self.x + X][0] != 0:
                            self.stop()
                            return True
    
    def _colisionR(self, board:np.ndarray[any], tempShape):
        for Y in range(self.shape.shape[0]):
                for X in range(self.shape.shape[1]):
                    if tempShape[Y, X] == 1:
                        if self.x + X < 0 or self.x + X >= board.shape[1] or board[self.y + Y, self.x + X][0] != 0:
                            return True
        return False

piezaIvar = Piece(shape_I, 1 , img.pieces["orangeBlack"]) 
piezaI = Piece(shape_I, 2,  img.pieces["orangeBlack"])
piezaL = Piece(shape_L, 3, img.pieces["greenBlue"])  
piezaLI = Piece(shape_LI, 4, img.pieces["red"])
piezaLvar = Piece(shape_L, 6, img.pieces["greenBlue"])
piezaSI = Piece(shape_SI, 5, img.pieces["orange"])
piezaO = Piece(shape_O, 7, img.pieces["yellow"], False)
piezaT = Piece(shape_T, 8, img.pieces["green"])
piezaTvar = Piece(shape_T, 9, img.pieces["green"])
piezaS = Piece(shape_S, 10, img.pieces["blue"])
piezaTmin = Piece(shape_Tmin, 11, img.pieces["purple"])
piezaImax = Piece(shape_Imax, 12, img.pieces["blueBlack"])

allPieces = [piezaIvar, piezaI, piezaL, piezaLI, piezaSI, piezaLvar, piezaO, piezaT, piezaTvar, piezaS, piezaTmin, piezaImax]
imgCompletePieces = [img.completePieces["orangeBlack"], img.completePieces["orangeBlack"], img.completePieces["green"], img.completePieces["red"], img.completePieces["orange"], img.completePieces["green"], img.completePieces["yellow"], img.completePieces["greenBlue"], img.completePieces["greenBlue"], img.completePieces["blue"], img.completePieces["purple"], img.completePieces["blueBlack"]]
imgCompletePiecesNum = [img.completePiecesNum[str(i)] for i in range(1,13)]

gv.activePieces = [True for _ in range(len(allPieces))]