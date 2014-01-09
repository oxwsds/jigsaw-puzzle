#!/usr/bin/env python

import pygame, sys, random
from pygame.locals import *


# Exit
def terminate():
    pygame.quit()
    sys.exit()


# Generate a new game board randomly
# If it isn't resolvable, then generate a new one.
def newGameBoard(cellNum):
    board = []
    for i in range(cellNum):
        board.append(i)

    random.shuffle(board)
    while not isResolvable(board):
        random.shuffle(board)

    return board


# Check if it can be done or not
def isResolvable(gameBoard):
    inversion = 0

    tmp = []
    for i in range(len(gameBoard)):
        tmp.append(gameBoard[i])
    tmp.remove(len(gameBoard) - 1)

    for i in range(0, len(tmp)):
        for j in range(i + 1, len(tmp)):
            if tmp[i] > tmp[j]:
                inversion += 1
    return inversion % 2 == 0


# Have it done?
def isFinish(gameBoard):
    for i in range(len(gameBoard)):
        if i != gameBoard[i]:
            return False
    return True


def runGame(vhNum):
    pygame.init()

    gameImage = pygame.image.load("00%d.png" % vhNum)

    gameRect = gameImage.get_rect()
    screen = pygame.display.set_mode((gameRect.width, gameRect.height))
    pygame.display.set_caption("%s*%s Jigsaw Puzzle" % (vhNum, vhNum))

    cellNum = vhNum * vhNum
    cellWidth = gameRect.width / vhNum
    cellHeight = gameRect.height / vhNum

    gameBoard = newGameBoard(cellNum)
    whiteCell = gameBoard.index(cellNum - 1)

    while True:

        if isFinish(gameBoard) and vhNum < 5:
            runGame(vhNum + 1)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    terminate()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                row = y / cellHeight
                col = x / cellWidth
                index = row * vhNum + col
                if (index == whiteCell - vhNum or index == whiteCell + vhNum
                    or (whiteCell % vhNum != vhNum -1 and index == whiteCell + 1)
                    or (whiteCell % vhNum != 0 and index == whiteCell - 1)):

                    gameBoard[index], gameBoard[whiteCell] = gameBoard[whiteCell], gameBoard[index]
                    whiteCell = index

        for i in range(vhNum + 1):
            pygame.draw.line(gameImage, (0, 0, 0), (0, i * cellHeight), (gameRect.width, i * cellHeight))
            pygame.draw.line(gameImage, (0, 0, 0), (cellWidth * i, 0), (cellWidth * i, gameRect.height))

        for i in range(cellNum):
            rowDst = i / vhNum
            colDst = i % vhNum
            rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

            rowSrc = gameBoard[i] / vhNum
            colSrc = gameBoard[i] % vhNum
            rectSrc = pygame.Rect(colSrc * cellWidth, rowSrc * cellHeight, cellWidth, cellHeight)

            screen.blit(gameImage, rectDst, rectSrc)

        pygame.display.update()

runGame(3)
