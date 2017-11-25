import pygame, sys
from pygame.locals import *
import numpy as np
import math

pygame.init()
pygame.display.set_caption('Thinking is dying')

FPS = 60
info = pygame.display.Info()
WINDOWWIDTH = int(info.current_w)
WINDOWHEIGHT = int(info.current_h*0.8)

DIM = 2
NORMWIDTH = WINDOWWIDTH/1920.
NORMHEIGHT = WINDOWHEIGHT/1080.

GAMEWINTOLERANCE = 10*NORMWIDTH

#gamestate
LEVEL = 0

#playerstats
HEALTHMAX=100
DEFAULTPOS = np.array([WINDOWWIDTH/4.,WINDOWHEIGHT/2.])


#controls
LEFT = (K_LEFT,K_a,K_h)
RIGHT = (K_RIGHT,K_d,K_l)
UP = (K_UP,K_w,K_k)
DOWN = (K_DOWN,K_s,K_j)

WHITE = (255,255,255)
BGCOLOR = (100,50,50)
BLACK = (0,0,0)
RED = (219,87,127)
GREEN = (102,129,248)
BLUE = (0,0,255)
ALPHATHRESHOLD = 5
#map
#nachestesLevel
GOONUP = (K_1,K_t)
GOONSTRAIGHT = (K_2,K_z)
GOONDOWN = (K_3,K_u)



#initial position
INITX = int(1720.*NORMWIDTH)
INITY = int(WINDOWHEIGHT-125.*NORMHEIGHT)


posx = INITX
posy = INITY


#pygame.key.set_repeat(5000//FPS,10000//FPS)

#init graphics

GFX = "./gfx/"


#keyboard array
#left right up down
inputKey=[0,0]

#tries going into wall
TRIES = 10
#grafics

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH , WINDOWHEIGHT))
DISPLAYSURF.fill(BGCOLOR)
BACKGROUND = pygame.transform.smoothscale(pygame.image.load(GFX+"neuronteil1.png"),(WINDOWWIDTH,WINDOWHEIGHT))
AXON = pygame.transform.smoothscale(pygame.image.load(GFX+"neuronteil2.png"),(WINDOWWIDTH,WINDOWHEIGHT))
MAP = pygame.transform.smoothscale(pygame.image.load(GFX+"map.png"),(WINDOWWIDTH,WINDOWHEIGHT))


