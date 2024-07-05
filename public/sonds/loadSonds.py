import os
from pygame.mixer import Sound
import pygame as pg
import globalVariables as gv
import threading

def fadeoutAndLoad(music):
    if pg.mixer.music.get_busy():
        pg.mixer.music.fadeout(1000)
        pg.time.wait(1000)
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(gv.volumen)
        pg.mixer.music.play(-1, 3.0, 1000)
    else:
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(gv.volumen)
        pg.mixer.music.play(-1, 3.0, 1000)

def playMusic(music:str):
    if not gv.activeSond or not gv.music: return

    music_thread = threading.Thread(target=fadeoutAndLoad, args=(music,))
    music_thread.start()
    

def stopMusic():
    if not gv.activeSond: return
    pg.mixer.music.fadeout(1000)

def upodateVolumen():
    if not gv.activeSond: return
    pg.mixer.music.set_volume(gv.volumen)

def loadMusicDict(directorio:str, end:str=".mp3"):
    sounds = []
    for file in os.listdir(directorio):
        if file.endswith(end):
            completePath = os.path.join(directorio, file)
            nombre_sin_extension = os.path.splitext(file)[0]
            sounds.append(completePath)
    return sounds

def loadSondDict(directorio:str, end:str=".mp3"):
    sounds = {}
    for file in os.listdir(directorio):
        if file.endswith(end):
            completePath = os.path.join(directorio, file)
            nombre_sin_extension = os.path.splitext(file)[0]
            sounds[nombre_sin_extension] = Sound(completePath)
    return sounds

music = loadMusicDict("public\\sonds\\music")
