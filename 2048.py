#!/usr/bin/python2


#
#############################################################################
#Name        : 2048
#Author      : Saket S Komawar
#Description : "2048" with GUI and Sound.
#############################################################################
#


#Modules
import pygame, sys, random, time
from pygame.locals import *


#Syntactic Sugars
FPS = 100
WINDOWWIDTH = 400
WINDOWHEIGHT = 450
MAINTILESIZE = 80
BOARDCOLUMNS = 4
BOARDROWS = 4
SIZE = 4 #equals BOARDCOLUMNS or BOARDROWS
FONTSIZE = 20
GAPSIZE = 10
SOUND = "2048.ogg"
TILESIZE = MAINTILESIZE - (GAPSIZE / 2)
XMARGIN = int((WINDOWWIDTH - (MAINTILESIZE * BOARDCOLUMNS)) / 2)
YMARGIN = int((WINDOWHEIGHT - (MAINTILESIZE * BOARDROWS)) / 2)


#Colors
#			R	 G	  B
WHITE   = (255, 255, 255)
GREY    = ( 71,  71,  71)
BLANK   = (235, 235, 235)


#Digit Colors		 Hex
TWO              = "eee4da"
FOUR             = "ede0c8"
EIGHT            = "f2b179"
SIXTEEN          = "5f9563"
THIRTYTWO        = "f67c5f"
SIXTYFOUR        = "f65e3b"
ONETWOEIGHT      = "edcf72"
TWOFIVESIX       = "edcc61"
FIVEONETWO       = "edc850"
ONEZEROTWOFOUR   = "edc53f"
TWOZEROFOUREIGHT = "edc22e"
OTHER            = "cdc1b4"


#Elements Color
#					R    G    B
BACKGROUNDCOLOR = (187, 173, 160)
TILEBGCOLOR     = (195, 180, 170)
SCORECOLOR      = (61, 50, 50)
DIGITCOLOR      = (61, 50, 50)


#Main Function
def main():
	#Global Declarations
	global DISPLAYSURF, FONTOBJECT, FPSCLOCKOBJ, SCORE

	#Start of Pygame
	pygame.init()
	
	#Setting of Main Window
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption("2048")

	#Setting Icon
	pygame.display.set_icon(pygame.image.load("2048.png"))
	
	#Setting FontObject
	FONTOBJECT = pygame.font.Font("freesansbold.ttf", FONTSIZE)
	
	#FpsClockObject
	FPSCLOCKOBJ = pygame.time.Clock()
	
	#Initialize MainBoard
	MainBoard = InitBoard()

	#Score Initialization
	SCORE = 0
	
	#Game Loop
	while True:
		#BackGroundColor and TileBgColor
		DISPLAYSURF.fill(BACKGROUNDCOLOR)
		pygame.draw.rect(DISPLAYSURF, TILEBGCOLOR, (XMARGIN, YMARGIN, BOARDCOLUMNS * MAINTILESIZE + (GAPSIZE / 2), BOARDROWS * MAINTILESIZE + (GAPSIZE / 2)))
		
		#Score Section
		textsurfobj, textrectobj = MakeText("Score:", SCORECOLOR, (YMARGIN + BOARDROWS * MAINTILESIZE), XMARGIN)
		DISPLAYSURF.blit(textsurfobj, textrectobj) 
		pygame.draw.rect(DISPLAYSURF, GREY, (3 * XMARGIN, YMARGIN + BOARDROWS * MAINTILESIZE + 3 * GAPSIZE / 2, 100, 40))
		textsurfobj = FONTOBJECT.render(str(SCORE), True, WHITE)
		textrectobj = textsurfobj.get_rect()
		textrectobj.center = (3 * XMARGIN + 50, YMARGIN + BOARDROWS * MAINTILESIZE + 3 * GAPSIZE / 2 + 20)
		DISPLAYSURF.blit(textsurfobj, textrectobj)
		
		#Drawing the Board
		DrawMainBoard(MainBoard)

		#Success Initialization	
		success = False

		#Event Handling Loop
		for event in pygame.event.get():
			if event.type == QUIT:
				terminator()
			elif event.type == KEYUP:#Handles KeyUp Events
				if event.key in (K_LEFT, K_a):
					success = MoveLeft(MainBoard)
				elif event.key in (K_RIGHT, K_d):
					success = MoveRight(MainBoard)
				elif event.key in (K_UP, K_w):
					success = MoveUp(MainBoard)
				elif event.key in (K_DOWN, K_s):
					success = MoveDown(MainBoard)
				if(success == True):
					PlaySound()
					AddRandom(MainBoard)

		#To Check the End of Game
		if(GameEnded(MainBoard)):
			terminator()

		pygame.display.update()
		FPSCLOCKOBJ.tick(FPS)


#Return TextSurfObj and TextRectObj
def MakeText(text, color, top, left):
	textsurfobj = FONTOBJECT.render(text, True, color)
	textrectobj = textsurfobj.get_rect()
	textrectobj.center = (left + (TILESIZE / 2), top + (TILESIZE / 2))
	return textsurfobj, textrectobj


#Return top and left of the Tile
def GetTopLeftOfTile(tilex, tiley):
	top = YMARGIN + (tiley - 1) * MAINTILESIZE + (GAPSIZE / 2)
	left = XMARGIN + (tilex - 1) * MAINTILESIZE + (GAPSIZE / 2)
	return top, left


#Return List of Lists with 0 as Initial Value and Fill 2 Random Blocks
def InitBoard():
	board = []
	for i in range(BOARDCOLUMNS):
		tmp = []
		for j in range(BOARDROWS):
			tmp.append(0)
		board.append(tmp)
	AddRandom(board)
	AddRandom(board)
	return board


#SlideUp
def SlideUp(grid):
	flag = [0, 0, 0, 0]
	success = False
	for i in range(SIZE):
		tmp = i
		j = 0
		while(j < i):
			if(grid[tmp] != 0):
				if(grid[tmp] == grid[tmp - 1] and flag[tmp - 1] == 0 and flag[tmp] == 0):
					grid[tmp - 1] = 2 * grid[tmp]
					global SCORE
					SCORE = SCORE + grid[tmp - 1]
					grid[tmp] = 0
					if(tmp - 1 == 0):
						flag[0] = 1
					elif(tmp - 1 == 1):
						flag[1] = 1
					elif(tmp - 1 == 2):
						flag[2] = 1
					success = True
				elif(grid[tmp - 1] == 0 and grid[tmp] != 0):
					grid[tmp - 1] = grid[tmp]
					grid[tmp] = 0
					success = True
			tmp -= 1
			j += 1
	return success


#MoveUp
def MoveUp(grid):
	success = False
	for i in range(SIZE):
		success |= SlideUp(grid[i])
	return success


#MoveDown
def MoveDown(grid):
	success = False
	for i in range(SIZE):
			tmp = grid[i][0]
			grid[i][0] = grid[i][3]
			grid[i][3] = tmp
			tmp = grid[i][1]
			grid[i][1] = grid[i][2]
			grid[i][2] = tmp
	for  i in range(SIZE):
		success |= SlideUp(grid[i])
	for i in range(SIZE):
			tmp = grid[i][0]
			grid[i][0] = grid[i][3]
			grid[i][3] = tmp
			tmp = grid[i][1]
			grid[i][1] = grid[i][2]
			grid[i][2] = tmp
	return success


#RotateBoard(AntiClockWise)
def RotateBoard(grid):
	n = SIZE
	i = 0
	while(i < n / 2):
		j = i
		while(j < n -i -1):
			tmp = grid[i][j]
			grid[i][j] = grid[j][n-i-1]
			grid[j][n-i-1] = grid[n-i-1][n-j-1]
			grid[n-i-1][n-j-1] = grid[n-j-1][i]
			grid[n-j-1][i] = tmp
			j += 1
		i += 1


#MoveLeft
def MoveLeft(grid):
	RotateBoard(grid)
	success = MoveUp(grid)
	RotateBoard(grid)
	RotateBoard(grid)
	RotateBoard(grid)
	return success


#MoveRight
def MoveRight(grid):
	RotateBoard(grid)
	RotateBoard(grid)
	RotateBoard(grid)
	success = MoveUp(grid)
	RotateBoard(grid)
	return success


#AddRandom
def AddRandom(board):
	length = 0
	mainlist = []
	for i in range(SIZE):
		for j in range(SIZE):
			t_list = []
			t_list.append(0)
			t_list.append(0)
			mainlist.append(t_list)
	for i in range(SIZE):
		for j in range(SIZE):
			if(board[i][j] == 0):
				mainlist[length][0] = i
				mainlist[length][1] = j
				length += 1
	if(length > 0):
		block = random.randint(1, 9999999999) % length
		n = 2 * int((random.randint(1, 9999999999) % 10) / 9 + 1)
		i = mainlist[block][0]
		j = mainlist[block][1]
		board[i][j] = n


#Return Tile Color
def TileColor(value):
	if(value == 0):
		return BLANK
	elif(value == 2):
		return RGB(TWO)
	elif(value == 4):
		return RGB(FOUR)
	elif(value == 8):
		return RGB(EIGHT)
	elif(value == 16):
		return RGB(SIXTEEN)
	elif(value == 32):
		return RGB(THIRTYTWO)
	elif(value == 64):
		return RGB(SIXTYFOUR)
	elif(value == 128):
		return RGB(ONETWOEIGHT)
	elif(value == 256):
		return RGB(TWOFIVESIX)
	elif(value == 512):
		return RGB(FIVEONETWO)
	elif(value == 1024):
		return RGB(ONEZEROTWOFOUR)
	elif(value == 2048):
		return RGB(TWOZEROFOUREIGHT)
	else:
		return RGB(OTHER)


#Return the MainBoard
def DrawMainBoard(board):
	for i in range(1, BOARDCOLUMNS + 1):
		for j in range(1, BOARDROWS + 1):
			top, left = GetTopLeftOfTile(i, j)
			tilecolor = (TileColor(board[i - 1][j - 1]))
			pygame.draw.rect(DISPLAYSURF, tilecolor, (left, top, TILESIZE, TILESIZE))
			if(board[i - 1][j - 1] != 0):
				textsurfobj, textrectobj = MakeText(str(board[i - 1][j - 1]), DIGITCOLOR, top, left)
			else:
				textsurfobj, textrectobj = MakeText("", DIGITCOLOR, top, left)
			DISPLAYSURF.blit(textsurfobj, textrectobj)
	pygame.display.update()


#Play Sound
def PlaySound():
	Beep = pygame.mixer.Sound(SOUND)
	Beep.play()


#Terminator Function
def terminator():
	pygame.quit()
	sys.exit()


#To FindPairs
def FindPairs(board):
	success = False
	for i in range(SIZE):
		j = 0
		while(j < SIZE - 1):
			if(board[i][j] == board[i][j + 1]):
				return True
			j += 1
	return success


#To Check the End
def GameEnded(board):
	success = True
	for i in range(SIZE):
		for j in range(SIZE):
			if(board[i][j] == 0):
				return False
	if(FindPairs(board)):
		return False
	RotateBoard(board)
	if(FindPairs(board)):
		success = False
	RotateBoard(board)
	RotateBoard(board)
	RotateBoard(board)
	return success


#Returns RGB tuple
def RGB(hexstr):
	R = int(hexstr[:2], 16)
	G = int(hexstr[2:4], 16)
	B = int(hexstr[4:], 16)
	return(R, G, B)


if __name__ == '__main__':
	main()