import os
from pygame import image

def loadImagesDict(directorio:str, end:str=".png"):
    images = {}
    for file in os.listdir(directorio):
        if file.endswith(end):  # Filtrar por files .png
            completePath = os.path.join(directorio, file)
            nombre_sin_extension = os.path.splitext(file)[0]
            images[nombre_sin_extension] = image.load(completePath)
    return images

pieces = loadImagesDict("public\\images\\pieces")
completePieces = loadImagesDict("public\\images\\completePieces")
completePiecesNum = loadImagesDict("public\\images\\completePiecesNum")
logos = loadImagesDict("public\\images\\logos")
ods = loadImagesDict("public\\images\\ods", ".jpg")
