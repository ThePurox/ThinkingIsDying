import pygame, sys
from pygame.locals import *
import numpy as np
import math
from constants import *



PLAYERIMG = pygame.image.load(GFX + 'player.png')
velmax = 2.
#pygame.draw.rect(DISPLAYSURF, RED, (30,50,300,400))
#pygame.draw.line(DISPLAYSURF, BLUE, (60,60),(120,60),4)

#weapon stats
meeledist = 30.
meeledamage = 1.
meelesprite = GFX + 'sword.png'
meelevel = 1.

gundamage = 0.5
gundist = 200
gunsprite = GFX + 'crossbow.png'
gunvel = 1.

def calcAngle(pos1, pos2):
    dx = pos2[0]*1.-pos1[0]*1.
    dy = pos2[1]*1.-pos1[1]*1.
    return math.atan2(dx,dy)*180./np.pi

class weapon:
    def __init__(self, type, pos):
        self.type = type
        self.angle = 0
        self.pos = np.copy(pos)
        self.inAnimation = False
        if( self.type == "meele" ):
            self.dist = meeledist
            self.attacRange = 50
            self.damage = meeledamage
            self.sprite = pygame.image.load(meelesprite)
            self.vel = meelevel
            self.frameMax=10
        if( self.type == "gun" ):
            dist = gundist
            self.attacRange = 50
            self.damage = gundamage
            self.sprite = pygame.image.load(gunsprite)
            self.vel = gunvel
            self.frameMax=5
        #self.pos[0] -= self.sprite.get_width()/2
        #self.pos[1] -= self.sprite.get_height()/2

    def animate(self,  defenderPos):
        dir = defenderPos - self.pos
        dist = np.linalg.norm(dir)
        if(self.frame <= self.frameMax/2.):
            self.pos += 2*dir/dist
        if(self.frame >= self.frameMax/2.):
            self.pos -= 2*dir/dist

        if(self.frame >= self.frameMax):
            self.inAnimation = False
            return False
        self.frame += 1
        return True

    def draw(self,enemyBool):
        if(enemyBool):
            phi = calcAngle(self.pos, player.pos) - self.angle
        else:
            phi = calcAngle(self.pos, pygame.mouse.get_pos()) - self.angle
        if(self.type == "meele"):
            sprite = meelesprite
        if(self.type == "gun"):
            sprite = gunsprite
        self.sprite = pygame.transform.rotate(pygame.image.load(sprite), self.angle)
        self.angle += phi

        self.pos[0] -= self.sprite.get_width()/2.
        self.pos[1] -= self.sprite.get_height()/2.
        DISPLAYSURF.blit(self.sprite, self.pos)
        self.pos[0] += self.sprite.get_width()/2.
        self.pos[1] += self.sprite.get_height()/2.

    def resetPos(self,pos):
        self.pos = np.copy(pos)


class entity:
    def __init__(self,pos):
        self.pos = np.copy(pos)


def boundary(pos):
    color = BACKGROUND.get_at(np.round(pos).astype(int))
    return color.a > ALPHATHRESHOLD
def boundary2(pos):
    color = AXON.get_at(np.round(pos).astype(int))
    return color.a > ALPHATHRESHOLD

class playerClass(entity):
    playerSprite = pygame.image.load(GFX + 'player.png')
    velmin=1.
    vel=np.zeros(2)
    frame = 0
    def levelUp(self):
        self.strength += 1
        self.health = HEALTHMAX
        self.pos = np.copy(DEFAULTPOS)
        self.vel = np.zeros(DIM)
        for wep in self.weapons:
            wep.pos = np.copy(self.pos)

    def addWeapon(self, weap):
        self.weapons.append(weap)
    def draw(self):
        for i in range(0,DIM):
            self.pos[i] -= self.playerSprite.get_width()/2.
        DISPLAYSURF.blit(self.playerSprite, self.pos)
        for i in range(0,DIM):
            self.pos[i] += self.playerSprite.get_width()/2.
        for weap in self.weapons:
            weap.draw(False)
    def move(self,lev):
        for i in range(0,DIM):
            if(inputKey[i] != 0 and player.vel[i]*inputKey[i] > 0):
                self.vel[i] += math.copysign(1,self.vel[i])*velmax*(np.exp(-abs(self.vel[i]/velmax)))
            if(inputKey[i] != 0 and player.vel[i]*inputKey[i] <= 0):
                self.vel[i] = math.copysign(self.velmin,inputKey[i])
            if(inputKey[i] == 0):
                self.vel[i] -= self.vel[i]*0.3

        for i in range(0,TRIES):
            if lev % 2 == 1:
                if boundary(self.pos+self.vel):
                    self.pos += self.vel
                    for weap in self.weapons:
                        weap.pos += self.vel
                    break
                else:
                    self.vel *= 0.7
            else:
                if boundary2(self.pos+self.vel):
                    self.pos += self.vel
                    for weap in self.weapons:
                        weap.pos += self.vel
                    break
                else:
                    self.vel *= 0.7


    def update(self,lev):
        self.move(lev)
        self.attac()
        self.draw()

    def attac(self):
        for weapon in self.weapons:
            if(weapon.inAnimation):
                if(weapon.animate(pygame.mouse.get_pos()) == False):
                    dir =  pygame.mouse.get_pos() - weapon.pos
                    attacpoint = self.pos + dir / np.linalg.norm(dir) /2. * weapon.attacRange
                    for enemy in enemyList:
                        if(np.linalg.norm(attacpoint - enemy.pos) <= weapon.attacRange/2.):
                            enemy.health -= player.strength * weapon.damage
                    weapon.pos = np.copy(self.pos)


    def __init__(self, health, strength, weapons, pos):
        self.health = health
        self.weapons = []
        self.strength = 1.
        #self.pos = pos
        entity.__init__(self,pos)
        for weap in weapons:
            self.addWeapon(weapon(weap,np.copy(self.pos)))
        #self.playerSprite = playerSprite



class enemy(entity):
    dir = []
    for i in range(0,DIM):
        dir.append(0)
    dist = 0
    def __init__(self, health, strength, intelligence, weap, pos):
        self.health = health
        self.strength= strength
        self.intl = intelligence
        #self.pos = pos
        entity.__init__(self,np.copy(pos))
        self.weapon = weapon(weap, np.copy(pos))
        if(self.weapon.type == "meele"):
            self.sprite = pygame.image.load(GFX + "enemy.png")
        if(self.weapon == "gun"):
            self.sprite.type = pygame.image.load(GFX + "gunEnemy.png")

    def update(self):
        self.calcDist()
        self.attac()
        self.move()
        self.draw()
        self.weapon.draw(True)

    def calcDist(self):
        self.dir = (player.pos-self.pos)
        self.dist = np.linalg.norm(self.dir)

    def move(self):
        if( self.dist <= self.weapon.dist ):
            return
        else:
            d=self.weapon.vel * (self.intl * self.dir/ self.dist  + (1. - self.intl)* 2.*(np.random.rand(DIM)-0.5 ))
            for i in range(0,TRIES):
                if boundary(self.pos+d):
                    self.pos += d
                    self.weapon.pos += d
                    break
                else:
                    d *= 0.7

    def draw(self):
        for i in range(0,DIM):
            self.pos[i] -= self.sprite.get_width()/2.
        DISPLAYSURF.blit(self.sprite, self.pos)
        for i in range(0,DIM):
            self.pos[i] += self.sprite.get_width()/2.

    def attac(self):
        if(self.weapon.inAnimation):
            if(self.weapon.animate(player.pos) == False):
                if(self.weapon.attacRange >= self.dist):
                    player.health -= self.weapon.damage * self.strength
                self.weapon.resetPos(self.pos)
        elif(self.dist <= self.weapon.attacRange):
            self.weapon.inAnimation = True
            self.weapon.frame = 0

#initialize player and enemyList

enemyList = []
player = playerClass(HEALTHMAX,1,["meele"],DEFAULTPOS)
