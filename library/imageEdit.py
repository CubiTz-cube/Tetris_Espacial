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

def lightImage(image, value):
    width, height = image.get_size()
    light_image = pg.Surface((width, height))
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))
            r = min(r + value, 255)
            g = min(g + value, 255)
            b = min(b + value, 255)
            light_image.set_at((x, y), (r, g, b, a))
    return light_image