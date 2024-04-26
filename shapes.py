import numpy as np

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

shape_D = np.zeros((3, 3), dtype=int)
shape_D[1, 0] = 1
shape_D[1, 1] = 1
shape_D[2, 1] = 1
shape_D[2, 2] = 1

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