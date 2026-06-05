# Goodie and GoodieMgr classes

import pygame
import pygwidgets
import random
from Constants import *
from DodgerObject import DodgerObject


class Goodie(DodgerObject):
    # Load the image once
    GOODIE_IMAGE = pygame.image.load('images/goodie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window

        # DodgerObject에서 size, radius 초기화
        self._init_size()

        self.y = random.randrange(0, GAME_HEIGHT - self.size)
        self.points = self.getPointsForSize()

        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])

        if self.direction == Goodie.LEFT:  # start on right side of the window
            self.x = WINDOW_WIDTH
            self.speed = -random.randrange(DodgerObject.MIN_SPEED,
                                           DodgerObject.MAX_SPEED + 1)
            self.minLeft = -self.size
        else:  # start on left side of the window
            self.x = 0 - self.size
            self.speed = random.randrange(DodgerObject.MIN_SPEED,
                                          DodgerObject.MAX_SPEED + 1)

        self.image = pygwidgets.Image(self.window,
                                      (self.x, self.y),
                                      Goodie.GOODIE_IMAGE)

        percent = int((self.size * 100) / DodgerObject.MAX_SIZE)
        self.image.scale(percent, False)

    def getPointsForSize(self):
        if self.size <= 20:
            return POINTS_FOR_SMALL_GOODIE
        elif self.size <= 30:
            return POINTS_FOR_MEDIUM_GOODIE
        else:
            return POINTS_FOR_LARGE_GOODIE

    def update(self):
        # Goodie 이동만 담당
        self.x = self.x + self.speed
        self.image.setLoc((self.x, self.y))

    def isOffScreen(self):
        # 삭제 조건만 따로 판단
        if self.direction == Goodie.LEFT:
            return self.x < self.minLeft
        else:
            return self.x > WINDOW_WIDTH

    def getScorePopupLoc(self):
        goodieRect = self.image.getRect()
        x = min(goodieRect.right + 5, WINDOW_WIDTH - 55)
        y = max(goodieRect.top - 5, 0)
        return x, y

    def getPoints(self):
        return self.points


class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 111

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goodiesList = []
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI

    def update(self, player_cx, player_cy, player_radius):
        # Goodie들을 움직이고,
        # 화면 밖으로 나간 Goodie와 플레이어와 충돌한 Goodie를 제거
        goodieHits = []
        survivors = []

        for oGoodie in self.goodiesList:
            oGoodie.update()

            # 1. 삭제 조건
            if oGoodie.isOffScreen():
                continue

            # 2. 충돌 조건
            elif oGoodie.collide(player_cx, player_cy, player_radius):
                goodieHits.append({
                    'loc': oGoodie.getScorePopupLoc(),
                    'points': oGoodie.getPoints()
                })

            # 3. 계속 남아 있을 Goodie
            else:
                survivors.append(oGoodie)

        self.goodiesList = survivors

        # 일정 프레임마다 새 Goodie 생성
        self.nFramesTilNextGoodie = self.nFramesTilNextGoodie - 1

        if self.nFramesTilNextGoodie == 0:
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.nFramesTilNextGoodie = random.randrange(
                GoodieMgr.GOODIE_RATE_LO,
                GoodieMgr.GOODIE_RATE_HI
            )

        return goodieHits

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()
