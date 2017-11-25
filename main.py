import pygame, sys
from pygame.locals import *
import numpy as np
import math
from constants import *
from playerEnemyClasses import *
import subprocess

#todo kampf system
#health bar
#crossbow
AUDIOACT = ['+','+','c','+','c']
AXONPOS = np.array([44.*NORMWIDTH, WINDOWHEIGHT - 620*NORMHEIGHT])
pygame.display.toggle_fullscreen()

def editor():
    call = ['nano', 'vim', 'nano', 'vim','mg'] #need to install mg editor
    if LEVEL > 1 and LEVEL-2 >= 0:
        pygame.display.toggle_fullscreen()
        quote = str((LEVEL-2)%6+1)
        quote = ' ./quotes/' + quote
        subprocess.call(call[(LEVEL-2)%len(call)]+quote,shell=True)
        pygame.display.toggle_fullscreen()

def drawmap():
    global posx
    global posy
    global LEVEL
    pygame.draw.circle(DISPLAYSURF, BLUE,(INITX,INITY), 3, 0)
    if(LEVEL % 2 == 1):
        if (player.pos[0] >= 0.9*WINDOWWIDTH and len(enemyList) == 0):
            levelInit()
    if LEVEL % 2 == 0:
        if math.sqrt((posx-1788.*NORMWIDTH)**2+(posy-WINDOWHEIGHT+91.*NORMHEIGHT)**2) < GAMEWINTOLERANCE:
            LEVEL = -2
            pygame.draw.circle(DISPLAYSURF, GREEN,(posx,posy), 3, 0)
            return
        if posx < int(1618*NORMWIDTH) or posx > int(1847*NORMWIDTH) or posy > int(WINDOWHEIGHT-52*NORMHEIGHT) or posy < int(WINDOWHEIGHT - 254*NORMHEIGHT):
            LEVEL = -1
        if len(enemyList) == 0:
            if int(1398.*NORMWIDTH) <=  player.pos[0] and player.pos[0] <= int(1663.*NORMWIDTH) and int(WINDOWHEIGHT - 704.*NORMHEIGHT) >=  player.pos[1] and player.pos[1] >= int(WINDOWHEIGHT - 867.*NORMHEIGHT):
                posy += -5
                levelInit()
            if int(1670.*NORMWIDTH) <=  player.pos[0] and player.pos[0] <= int(2079.*NORMWIDTH) and int(WINDOWHEIGHT - 331.*NORMHEIGHT) >=  player.pos[1] and player.pos[1] >= int(WINDOWHEIGHT - 740.*NORMHEIGHT):
                posx += 5
                levelInit()
            if int(1415.*NORMWIDTH) <=  player.pos[0] and player.pos[0] <= int(1611.*NORMWIDTH) and int(WINDOWHEIGHT - 293.*NORMHEIGHT) >=  player.pos[1] and player.pos[1] >= int(WINDOWHEIGHT - 457.*NORMHEIGHT):
                posy += 5
                levelInit()
    pygame.draw.circle(DISPLAYSURF, GREEN,(posx,posy), 3, 0)
    pygame.draw.rect(DISPLAYSURF, RED,(10,int(WINDOWHEIGHT-10),int(WINDOWWIDTH/4), 10))
    pygame.draw.rect(DISPLAYSURF, GREEN,(10,int(WINDOWHEIGHT-10),int(WINDOWWIDTH/4.*player.health/HEALTHMAX), 10))








#myenemy = enemy(1,1,0.5,"meele",[350.,340.])
#enemyList.append(myenemy)

def levelInit():
    global LEVEL
    global BACKGROUND
    LEVEL += 1
    if(LEVEL % 2 == 1):
        BACKGROUND = pygame.transform.smoothscale(pygame.image.load(GFX+"neuronteil1.png"),(WINDOWWIDTH,WINDOWHEIGHT))
        for i in range(0,LEVEL):
            enpos = WINDOWHEIGHT*np.random.rand(DIM)
            while(boundary(enpos) == False):
                enpos = WINDOWHEIGHT*np.random.rand(DIM)
            enemyList.append(enemy(LEVEL,LEVEL,1-1./LEVEL,"meele",np.copy(enpos)))
        player.levelUp()
    else:
        BACKGROUND = pygame.transform.smoothscale(pygame.image.load(GFX+"neuronteil2.png"),(WINDOWWIDTH,WINDOWHEIGHT))
        player.pos = np.copy(AXONPOS)
        player.vel = np.zeros(DIM)
        for wea in player.weapons:
            wea.pos = np.copy(AXONPOS)


    if LEVEL >= 0:
        AUDIO = open('./tunechip/audio', 'w')
        AUDIO.write(AUDIOACT[LEVEL%len(AUDIOACT)])
    editor()

def terminate():
    subprocess.call("killall -s 9 python2",shell=True)
    pygame.quit()
    sys.exit()

def doGameStep():
    global posx,posy, LEVEL
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(MAP,(0,0))
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    for enemy in enemyList:
        enemy.update()
    for event in pygame.event.get():
        global inputKey
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
            terminate()
        if event.type == KEYDOWN:
            if event.key in LEFT:
                inputKey[0] += -1
            if event.key in RIGHT:
                inputKey[0] += 1
            if event.key in UP:
                inputKey[1] += -1
            if event.key in DOWN:
                inputKey[1] += 1
        if event.type == KEYUP:
            if event.key in LEFT:
                inputKey[0] += 1
            if event.key in RIGHT:
                inputKey[0] += -1
            if event.key in UP:
                inputKey[1] += 1
            if event.key in DOWN:
                inputKey[1] += -1
            if event.key in GOONUP:
                posy += -5
            if event.key in GOONDOWN:
                posy += 5
            if event.key in GOONSTRAIGHT:
                posx += 5
    for i in range(0,len(player.weapons)):
        if(pygame.mouse.get_pressed()[i] and (player.weapons[i].inAnimation == False)):
            player.weapons[i].inAnimation = True
            player.weapons[i].frame = 0
    if player.health <= 0:
        LEVEL = -1


    player.update(LEVEL)
    for enemy in enemyList:
        if(enemy.health <= 0):
            enemyList.remove(enemy)
    drawmap()

while True:
    if(LEVEL == 0):
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(pygame.transform.smoothscale(pygame.image.load(GFX+"story1.png"),(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
        for event in pygame.event.get():
            if event.type == KEYUP:
                LEVEL = -3
                continue
    if LEVEL == -3:
        DISPLAYSURF.blit(pygame.transform.smoothscale(pygame.image.load(GFX+"controls.png"),(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
        for event in pygame.event.get():
            if event.type == KEYUP:
                LEVEL = 0
                levelInit()
                continue
    if(LEVEL > 0):
        doGameStep()
    if(LEVEL == -1):
        DISPLAYSURF.blit(pygame.transform.smoothscale(pygame.image.load(GFX+"story5.png"),(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                terminate()
    if(LEVEL == -2):
        DISPLAYSURF.blit(pygame.transform.smoothscale(pygame.image.load(GFX+"story4.png"),(WINDOWWIDTH,WINDOWHEIGHT)),(0,0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                terminate()


    pygame.display.update()




