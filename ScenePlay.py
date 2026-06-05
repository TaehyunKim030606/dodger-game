import pygame
from pygame.locals import *
import pygwidgets
import pyghelpers
from Player import Player
from Baddies import BaddieMgr
from Goodies import GoodieMgr
from PowerUps import PowerUpMgr, POWER_UP_SHRINK, POWER_UP_INVINCIBLE
from Constants import *


class GameOverDialog:

    def __init__(self, window):
        self.window = window
        self.background = pygwidgets.Image(
            window, (40, 250), 'images/dialog.png')
        self.promptText = pygwidgets.DisplayText(
            window, (0, 290), '',
            width=WINDOW_WIDTH, justified='center', fontSize=36)
        self.yesButton = pygwidgets.CustomButton(
            window, (320, 370),
            'images/gotoHighScoresNormal.png',
            over='images/gotoHighScoresOver.png',
            down='images/gotoHighScoresDown.png',
            disabled='images/gotoHighScoresDisabled.png')
        self.noButton = pygwidgets.CustomButton(
            window, (62, 370),
            'images/noThanksNormal.png',
            over='images/noThanksOver.png',
            down='images/noThanksDown.png',
            disabled='images/noThanksDisabled.png')

    def show(self, message):
        self.promptText.setValue(message)
        return pyghelpers.customYesNoDialog(
            self.window, self.background,
            self.promptText, self.yesButton, self.noButton)


BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH, WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'game over'
SCORE_POPUP_FRAMES = 30
SCORE_POPUP_COLOR = (0, 255, 0)
POWER_UP_DURATION_MS = 8000


class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window = window

        self.controlsBackground = pygwidgets.Image(self.window,
                                                    (0, GAME_HEIGHT),
                                                    'images/controlsBackground.jpg')
        self.quitButton = pygwidgets.CustomButton(self.window,
                                                   (30, GAME_HEIGHT + 90),
                                                   up='images/quitNormal.png',
                                                   down='images/quitDown.png',
                                                   over='images/quitOver.png',
                                                   disabled='images/quitDisabled.png')
        self.highScoresButton = pygwidgets.CustomButton(self.window,
                                                         (190, GAME_HEIGHT + 90),
                                                         up='images/gotoHighScoresNormal.png',
                                                         down='images/gotoHighScoresDown.png',
                                                         over='images/gotoHighScoresOver.png',
                                                         disabled='images/gotoHighScoresDisabled.png')
        self.newGameButton = pygwidgets.CustomButton(self.window,
                                                      (450, GAME_HEIGHT + 90),
                                                      up='images/startNewNormal.png',
                                                      down='images/startNewDown.png',
                                                      over='images/startNewOver.png',
                                                      disabled='images/startNewDisabled.png',
                                                      enterToActivate=True)
        self.soundCheckBox = pygwidgets.TextCheckBox(self.window,
                                                      (380, GAME_HEIGHT + 68),
                                                      'Background music',
                                                      True, textColor=WHITE)
        self.gameOverImage = pygwidgets.Image(self.window, (140, 180),
                                               'images/gameOver.png')
        self.scoreTitleText = pygwidgets.DisplayText(self.window,
                                                      (38, GAME_HEIGHT + 17),
                                                      'Score:',
                                                      fontSize=24, textColor=WHITE)
        self.highScoreTitleText = pygwidgets.DisplayText(self.window,
                                                          (205, GAME_HEIGHT + 17),
                                                          'High Score:',
                                                          fontSize=24, textColor=WHITE)
        self.difficultyTitleText = pygwidgets.DisplayText(self.window,
                                                           (425, GAME_HEIGHT + 17),
                                                           'Level:',
                                                           fontSize=24, textColor=WHITE)
        self.scoreText = pygwidgets.DisplayText(self.window,
                                                 (55, GAME_HEIGHT + 47), '0',
                                                 fontSize=36, textColor=WHITE)
        self.highScoreText = pygwidgets.DisplayText(self.window,
                                                     (255, GAME_HEIGHT + 47), '',
                                                     fontSize=36, textColor=WHITE)
        self.difficultyText = pygwidgets.DisplayText(self.window,
                                                      (450, GAME_HEIGHT + 47), '1',
                                                      fontSize=36, textColor=WHITE)

        pygame.mixer.music.load('sounds/background.mid')
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameover.wav')
        self.scorePopupFont = pygame.font.Font(None, 32)
        self.pauseTitleFont = pygame.font.Font(None, 72)
        self.pauseHelpFont = pygame.font.Font(None, 32)

        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)
        self.oPowerUpMgr = PowerUpMgr(self.window)
        self.oDialog = GameOverDialog(self.window)

        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.backgroundMusic = True
        self.score = 0
        self.scorePopups = []
        self.shrinkEndTicks = 0
        self.invincibleEndTicks = 0
        self.gameStartTicks = 0
        self.pauseStartTicks = 0
        self.difficultyLevel = 1
        self.playingState = STATE_WAITING

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        self.getHiAndLowScores()

    def getHiAndLowScores(self):
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict['lowest']

    def reset(self):
        self.score = 0
        self.scoreText.setValue(self.score)
        self.scorePopups = []
        self.shrinkEndTicks = 0
        self.invincibleEndTicks = 0
        self.gameStartTicks = pygame.time.get_ticks()
        self.pauseStartTicks = 0
        self.difficultyLevel = 1
        self.difficultyText.setValue(self.difficultyLevel)
        self.getHiAndLowScores()
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()
        self.oPowerUpMgr.reset()
        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == KEYDOWN and event.key == K_p:
                if self.playingState == STATE_PLAYING:
                    self._pauseGame()
                elif self.playingState == STATE_PAUSED:
                    self._resumeGame()
                continue

            if self.playingState in (STATE_PLAYING, STATE_PAUSED):
                continue

            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING
            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)
            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue()
            if self.quitButton.handleEvent(event):
                self.quit()

    def _pauseGame(self):
        self.pauseStartTicks = pygame.time.get_ticks()
        self.playingState = STATE_PAUSED
        pygame.mouse.set_visible(True)
        pygame.mixer.music.pause()

    def _resumeGame(self):
        pausedDuration = pygame.time.get_ticks() - self.pauseStartTicks
        self.gameStartTicks += pausedDuration
        if self.shrinkEndTicks > 0:
            self.shrinkEndTicks += pausedDuration
        if self.invincibleEndTicks > 0:
            self.invincibleEndTicks += pausedDuration
        self.pauseStartTicks = 0
        self.playingState = STATE_PLAYING
        pygame.mouse.set_visible(False)
        if self.backgroundMusic:
            pygame.mixer.music.unpause()

    def update(self):
        if self.playingState != STATE_PLAYING:
            return

        nowTicks = pygame.time.get_ticks()
        mouseX, mouseY = pygame.mouse.get_pos()
        cx, cy, radius = self.oPlayer.update(mouseX, mouseY)

        if nowTicks < self.shrinkEndTicks:
            radius = radius / 2

        self._update_difficulty(nowTicks)
        self._update_score(cx, cy, radius, nowTicks)
        self._update_powerups(cx, cy, radius, nowTicks)

        isInvincible = nowTicks < self.invincibleEndTicks
        if (not isInvincible) and self.oBaddieMgr.hasPlayerHitBaddie(cx, cy, radius):
            self._handle_game_over()

    def _update_difficulty(self, nowTicks):
        elapsedSeconds = (nowTicks - self.gameStartTicks) // 1000
        self.difficultyLevel = min(MAX_DIFFICULTY_LEVEL,
                                   (elapsedSeconds // SECONDS_PER_DIFFICULTY_LEVEL) + 1)
        self.difficultyText.setValue(self.difficultyLevel)

    def _update_score(self, cx, cy, radius, nowTicks):
        goodieHits = self.oGoodieMgr.update(cx, cy, radius)
        if len(goodieHits) > 0:
            self.dingSound.play()
            for goodieHit in goodieHits:
                x, y = goodieHit['loc']
                points = goodieHit['points']
                self.score += points
                self.scorePopups.append({'x': x, 'y': y,
                                         'points': points,
                                         'framesLeft': SCORE_POPUP_FRAMES})

        nBaddiesEvaded = self.oBaddieMgr.update(self.difficultyLevel)
        self.score += nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED
        self.scoreText.setValue(self.score)

        for scorePopup in self.scorePopups.copy():
            scorePopup['framesLeft'] -= 1
            scorePopup['y'] -= 1
            if scorePopup['framesLeft'] <= 0:
                self.scorePopups.remove(scorePopup)

    def _update_powerups(self, cx, cy, radius, nowTicks):
        powerUpsHit = self.oPowerUpMgr.update(cx, cy, radius)
        for powerUpHit in powerUpsHit:
            if powerUpHit == POWER_UP_SHRINK:
                self.shrinkEndTicks = nowTicks + POWER_UP_DURATION_MS
            elif powerUpHit == POWER_UP_INVINCIBLE:
                self.invincibleEndTicks = nowTicks + POWER_UP_DURATION_MS

    def _handle_game_over(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        self.draw()

        if self.score > self.lowestHighScore:
            self._prompt_high_score()

        self._enable_ui()

    def _prompt_high_score(self):
        score_str = f'Your score: {self.score}\n'
        if self.score > self.highestHighScore:
            dialog_text = score_str + 'is a new high score, CONGRATULATIONS!'
        else:
            dialog_text = score_str + 'gets you on the high scores list.'

        if self.oDialog.show(dialog_text):
            self.goToScene(SCENE_HIGH_SCORES, self.score)

    def _enable_ui(self):
        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()

    def draw(self):
        self.window.fill(BLACK)
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
        self.oPowerUpMgr.draw()
        self.oPlayer.draw()

        for scorePopup in self.scorePopups:
            popupSurface = self.scorePopupFont.render('+' + str(scorePopup['points']),
                                                      True, SCORE_POPUP_COLOR)
            self.window.blit(popupSurface, (scorePopup['x'], scorePopup['y']))

        self.controlsBackground.draw()
        self.scoreTitleText.draw()
        self.highScoreTitleText.draw()
        self.difficultyTitleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.difficultyText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()

        if self.playingState == STATE_PAUSED:
            overlay = pygame.Surface((WINDOW_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.window.blit(overlay, (0, 0))
            pauseSurface = self.pauseTitleFont.render('PAUSED', True, WHITE)
            pauseRect = pauseSurface.get_rect(center=(WINDOW_WIDTH // 2,
                                                      GAME_HEIGHT // 2 - 20))
            self.window.blit(pauseSurface, pauseRect)
            helpSurface = self.pauseHelpFont.render('Press P to resume', True, WHITE)
            helpRect = helpSurface.get_rect(center=(WINDOW_WIDTH // 2,
                                                    GAME_HEIGHT // 2 + 35))
            self.window.blit(helpSurface, helpRect)

        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def leave(self):
        pygame.mixer.music.stop()
