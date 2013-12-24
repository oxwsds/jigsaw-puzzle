#!/usr/bin/env python

import pygame, sys, random
from pygame.locals import *


# set up some variables
VHNUM = 3
CELLNUM = VHNUM * VHNUM


# Exit
def terminate():
    pygame.quit()
    sys.exit()


# Generate a new game board randomly
# If it isn't resolvable, then generate a new one.
def newGameBoard():
    board = []
    for i in range(CELLNUM):
        board.append(i)

    random.shuffle(board)
    while not isResolvable(board):
        random.shuffle(board)

    return board


# Check if it can be done or not
def isResolvable(board):
    inversion = 0

    tmp = []
    for i in range(0, len(board)):
        tmp.append(board[i])
    tmp.remove(8)

    for i in range(0, len(tmp)):
        for j in range(i + 1, len(tmp)):
            if tmp[i] > tmp[j]:
                inversion += 1
    return inversion % 2 == 0



# Have it done?
def isFinish():
    for i in range(CELLNUM):
        if i != gameBoard[i]:
            return False
    return True


pygame.init()


# images
gameImage = pygame.image.load("_001.png")
gameRect = gameImage.get_rect()


# Set up the window
screen = pygame.display.set_mode((gameRect.width, gameRect.height))
pygame.display.set_caption("Jigsaw Puzzle")

#screen.blit(background, backgroundRect)


cellWidth = gameRect.width / VHNUM
cellHeight = gameRect.height / VHNUM

gameBoard = newGameBoard()
whiteCell = gameBoard.index(CELLNUM - 1)


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                terminate()

        if isFinish():
            continue

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            row = y / cellHeight
            col = x / cellWidth
            index = row * VHNUM + col
            if (index == whiteCell - VHNUM or index == whiteCell + VHNUM
                or (whiteCell % VHNUM != VHNUM -1 and index == whiteCell + 1)
                or (whiteCell % VHNUM != 0 and index == whiteCell - 1)):

                gameBoard[index], gameBoard[whiteCell] = gameBoard[whiteCell], gameBoard[index]
                whiteCell = index



    for i in range(VHNUM + 1):
        pygame.draw.line(gameImage, (0, 0, 0), (0, i * cellHeight), (gameRect.width, i * cellHeight))
        pygame.draw.line(gameImage, (0, 0, 0), (cellWidth * i, 0), (cellWidth * i, gameRect.height))

    for i in range(CELLNUM):
        rowDst = i / VHNUM
        colDst = i % VHNUM
        rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

        rowSrc = gameBoard[i] / VHNUM
        colSrc = gameBoard[i] % VHNUM
        rectSrc = pygame.Rect(colSrc * cellWidth, rowSrc * cellHeight, cellWidth, cellHeight)

        screen.blit(gameImage, rectDst, rectSrc)


    pygame.display.update()
