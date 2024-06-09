import pygame as pg

def convertImgToBn(image):
    width, height = image.get_size()
    bn_image = pg.Surface((width, height))
    for x in range(width):
        for y in range(height):
            r, g, b, _ = image.get_at((x, y))
            gris = (r + g + b) // 3
            bn_image.set_at((x, y), (gris, gris, gris))
    return bn_image