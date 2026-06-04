# Player
import pygame
import pygwidgets
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.loc = (-100, -100)
        self.normalSurface = pygame.image.load('images/player.png').convert_alpha()
        normalRect = self.normalSurface.get_rect()
        smallSize = (normalRect.width // 2, normalRect.height // 2)
        self.smallSurface = pygame.transform.scale(self.normalSurface, smallSize)
        self.isSmall = False
        self.image = pygwidgets.Image(window, self.loc, self.normalSurface)
        playerRect = self.image.getRect()
        self.maxX = WINDOW_WIDTH - playerRect.width
        self.maxY = GAME_HEIGHT - playerRect.height

    def setSmall(self, shouldBeSmall):
        if self.isSmall == shouldBeSmall:
            return

        self.isSmall = shouldBeSmall
        playerRect = self.image.getRect()
        self.loc = playerRect.topleft
        if self.isSmall:
            surface = self.smallSurface
        else:
            surface = self.normalSurface

        self.image = pygwidgets.Image(self.window, self.loc, surface)
        playerRect = self.image.getRect()
        self.maxX = WINDOW_WIDTH - playerRect.width
        self.maxY = GAME_HEIGHT - playerRect.height

    # Every frame, move the Player icon to the mouse position
    # Limits the x- and y-coordinates to the game area of the window
    def update(self, x, y):
        if x < 0:
            x = 0
        elif x > self.maxX:
            x = self.maxX
        if y < 0:
            y = 0
        elif y > self.maxY:
            y = self.maxY

        self.loc = (x, y)
        self.image.setLoc(self.loc)
        return self.image.getRect()

    def draw(self, isInvincible=False):
        self.image.draw()
        if isInvincible:
            playerRect = self.image.getRect()
            pygame.draw.rect(self.window, (255, 255, 0),
                             playerRect.inflate(8, 8), 3)
