# PowerUp and PowerUpMgr classes

import pygame
import random
import math
from Constants import *

POWER_UP_SHRINK = 'shrink'
POWER_UP_INVINCIBLE = 'invincible'


class PowerUp():
    SIZE = 32
    MIN_SPEED = 2
    MAX_SPEED = 5
    SHRINK_COLOR = (0, 150, 255)
    INVINCIBLE_COLOR = (255, 215, 0)

    def __init__(self, window):
        self.window = window
        self.kind = random.choice([POWER_UP_SHRINK, POWER_UP_INVINCIBLE])
        self.x = random.randrange(0, WINDOW_WIDTH - PowerUp.SIZE)
        self.y = 0 - PowerUp.SIZE
        self.speed = random.randrange(PowerUp.MIN_SPEED, PowerUp.MAX_SPEED + 1)
        self.rect = pygame.Rect(self.x, self.y, PowerUp.SIZE, PowerUp.SIZE)
        self.font = pygame.font.Font(None, 28)

    def update(self):
        self.y = self.y + self.speed
        self.rect.topleft = (self.x, self.y)

        return self.y > GAME_HEIGHT

    def draw(self):
        if self.kind == POWER_UP_SHRINK:
            color = PowerUp.SHRINK_COLOR
            label = 'S'
        else:
            color = PowerUp.INVINCIBLE_COLOR
            label = 'I'

        pygame.draw.ellipse(self.window, color, self.rect)
        pygame.draw.ellipse(self.window, WHITE, self.rect, 2)

        labelSurface = self.font.render(label, True, BLACK)
        labelRect = labelSurface.get_rect(center=self.rect.center)
        self.window.blit(labelSurface, labelRect)

    def collide(self, player_cx, player_cy, player_radius):
        powerup_cx = self.rect.centerx
        powerup_cy = self.rect.centery
        powerup_radius = self.rect.width // 2

        distance = math.hypot(
            player_cx - powerup_cx,
            player_cy - powerup_cy
        )

        return distance < player_radius + powerup_radius


class PowerUpMgr():
    POWER_UP_RATE_LO = 320
    POWER_UP_RATE_HI = 560

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.powerUpsList = []
        self.nFramesTilNextPowerUp = random.randrange(
            PowerUpMgr.POWER_UP_RATE_LO,
            PowerUpMgr.POWER_UP_RATE_HI
        )

    def update(self, player_cx, player_cy, player_radius):
        powerUpsHit = []

        powerUpsListCopy = self.powerUpsList.copy()

        for oPowerUp in powerUpsListCopy:
            deleteMe = oPowerUp.update()

            if deleteMe:
                self.powerUpsList.remove(oPowerUp)

            elif oPowerUp.collide(player_cx, player_cy, player_radius):
                powerUpsHit.append(oPowerUp.kind)
                self.powerUpsList.remove(oPowerUp)

        self.nFramesTilNextPowerUp = self.nFramesTilNextPowerUp - 1

        if self.nFramesTilNextPowerUp == 0:
            self.powerUpsList.append(PowerUp(self.window))
            self.nFramesTilNextPowerUp = random.randrange(
                PowerUpMgr.POWER_UP_RATE_LO,
                PowerUpMgr.POWER_UP_RATE_HI
            )

        return powerUpsHit

    def draw(self):
        for oPowerUp in self.powerUpsList:
            oPowerUp.draw()
