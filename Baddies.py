# Baddie and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import *
from DodgerObject import DodgerObject


class Baddie(DodgerObject):
    # Load the image only once
    BADDIE_IMAGE = pygame.image.load('images/baddie.png')

    def __init__(self, window):
        self.window = window
        self._init_size()  # sets self.size, self.radius
        self.x = random.randrange(0, WINDOW_WIDTH - self.size)
        self.y = 0 - self.size  # start above the window
        self.image = pygwidgets.Image(self.window, (self.x, self.y),
                                      Baddie.BADDIE_IMAGE)
        percent = (self.size * 100) / DodgerObject.MAX_SIZE
        self.image.scale(percent, False)
        self.speed = random.randrange(DodgerObject.MIN_SPEED,
                                      DodgerObject.MAX_SPEED + 1)

    def update(self):
        """Move the Baddie down. Returns True if it fell off the bottom."""
        self.y += self.speed
        self.image.setLoc((self.x, self.y))
        return self.y > GAME_HEIGHT


class BaddieMgr:
    ADD_NEW_BADDIE_RATE = 8  # frames between new Baddies

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

    def update(self):
        """Move all Baddies; remove those that fell off. Returns count removed."""
        survivors = []
        nBaddiesRemoved = 0
        for oBaddie in self.baddiesList:
            if oBaddie.update():
                nBaddiesRemoved += 1
            else:
                survivors.append(oBaddie)
        self.baddiesList = survivors

        self.nFramesTilNextBaddie -= 1
        if self.nFramesTilNextBaddie == 0:
            self.baddiesList.append(Baddie(self.window))
            self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

        return nBaddiesRemoved

    def draw(self):
        for oBaddie in self.baddiesList:
            oBaddie.draw()

    def hasPlayerHitBaddie(self, player_cx, player_cy, player_radius):
        """Circle-based collision check against all Baddies."""
        return any(b.collide(player_cx, player_cy, player_radius)
                   for b in self.baddiesList)
