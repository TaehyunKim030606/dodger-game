# Baddie and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import *
from DodgerObject import DodgerObject


class Baddie(DodgerObject):
    # Load the image once
    BADDIE_IMAGE = pygame.image.load('images/baddie.png')

    def __init__(self, window, difficultyLevel=1):
        self.window = window

        # DodgerObject에서 size, radius 초기화
        self._init_size()

        self.x = random.randrange(0, WINDOW_WIDTH - self.size)
        self.y = 0 - self.size

        speedBonus = max(0, difficultyLevel - 1)
        self.speed = random.randrange(DodgerObject.MIN_SPEED,
                                      DodgerObject.MAX_SPEED + 1) + speedBonus

        self.image = pygwidgets.Image(self.window,
                                      (self.x, self.y),
                                      Baddie.BADDIE_IMAGE)

        percent = int((self.size * 100) / DodgerObject.MAX_SIZE)
        self.image.scale(percent, False)

    def update(self):
        # Baddie 이동만 담당
        self.y = self.y + self.speed
        self.image.setLoc((self.x, self.y))

    def isOffScreen(self):
        # 삭제 조건만 따로 판단
        return self.y > GAME_HEIGHT


class BaddieMgr():
    BADDIE_RATE_LO = 15
    BADDIE_RATE_HI = 45

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.BADDIE_RATE_HI

    def update(self, player_cx, player_cy, player_radius, difficultyLevel=1):
        # Baddie들을 움직이고,
        # 화면 밖으로 나간 Baddie와 플레이어와 충돌한 Baddie를 제거

        nBaddiesHit = 0
        nBaddiesEvaded = 0
        survivors = []

        for oBaddie in self.baddiesList:
            oBaddie.update()

            # 1. 삭제 조건
            if oBaddie.isOffScreen():
                nBaddiesEvaded = nBaddiesEvaded + 1

            # 2. 충돌 조건
            elif oBaddie.collide(player_cx, player_cy, player_radius):
                nBaddiesHit = nBaddiesHit + 1

            # 3. 계속 남아 있을 Baddie
            else:
                survivors.append(oBaddie)

        self.baddiesList = survivors

        # 일정 프레임마다 새 Baddie 생성
        self.nFramesTilNextBaddie = self.nFramesTilNextBaddie - 1

        if self.nFramesTilNextBaddie == 0:
            oBaddie = Baddie(self.window, difficultyLevel)
            self.baddiesList.append(oBaddie)

            rateReduction = max(0, difficultyLevel - 1) * 2
            rateLo = max(5, BaddieMgr.BADDIE_RATE_LO - rateReduction)
            rateHi = max(rateLo + 1, BaddieMgr.BADDIE_RATE_HI - rateReduction)

            self.nFramesTilNextBaddie = random.randrange(
                rateLo,
                rateHi
            )

        return nBaddiesHit, nBaddiesEvaded

    def draw(self):
        for oBaddie in self.baddiesList:
            oBaddie.draw()
