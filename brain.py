import os, sys, time
import win32api, win32con
from PIL import ImageGrab
from PIL import ImageOps
import numpy as np

import imGrab

import coords

debugMode = True

#PLAYER INFO
playerSize = 36 # Square
playerBorder =  6 # Border thickness

#ENVIRONMENT INFO
headerSizeY = 100 #Only black = 70. Extra pixels added to fit the grid better,
gridSize = 50
# --- colors
background = (170, 165, 255)
safezone = (158, 242, 155)
gridA = (248, 247, 255)
gridB = (224, 218, 254)
player = (255, 0, 0)

#INPUTS
def Click(buttonCoord, func=""):
	win32api.SetCursorPos(buttonCoord)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(.2)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(.2)
	if (debugMode):
		print ("Click " + func)

#VISION
def FindPlayer():
	
	'''
	FIND THE PLAYER
	To be run at the start of every level. Further movement will depend
	on the coordinates returned by this method.
	'''

	print("")
	print("Started looking for player")

	#Find the players general area by screencaping portions of the screen and looking for red.
	found = False
	playerPos = (0, 0)
	xpad, ypad = 0, headerSizeY
	itrv = 36
	while (not found):
		img = imGrab.portionGrab(itrv, itrv, xpad, ypad)
		im = img.getcolors()
		for i in im:
			if (i[1][0] == 255 and i[1][1] == 0 and i[1][2] == 0):
				print(str(i[1][0]) + ", " + str(i[1][1]) + ", " + str(i[1][2]))
				found = True
				if (debugMode):
					print("Character found in quadrant " + str(xpad) +", "+ str(ypad))
				break
		if (not found):
			xpad += itrv
			if (xpad >= imGrab.xEnd):
				xpad = 0
				ypad += itrv
				print("...")
			#print (str(xpad) + ", " + str(ypad))

	#Find player in the quadrant by looking pixel by pixel
	pFound = False
	xp, yp = 0, 0
	while (not pFound):
		xy = (xp, yp) #current pixel to check
		i = img.getpixel(xy)
		if (i[0] == 255 and i[1] == 0 and i[2] == 0):
			#Player found. Player pos is adjusted to inlclude dark red border
			pFound = True
			playerPos = (xpad + xp - playerBorder, ypad + yp - playerBorder)
			print("Player found at " + str(playerPos[0]) + ", " + str(playerPos[1]))
		if (not pFound):
			xp += 1
			if (xp >= itrv):
				xp = 0
				yp += 1

	return playerPos

def GraphLevel():

	'''
	FIND the SHAPE of the level.
	To be used for path finding.

	'''

	print("")
	print("Started creating level grid.")

	grid = np.zeros((11, 20), int)
	level = 0

	#Define point to start searching 
	xp = gridSize/2 #Add half of grid size - evaluate the middle of the cell 
	yp = headerSizeY + (gridSize/2) #Add the header size

	xInd, yInd = -1, -1 #current cell index

	im = imGrab.screenGrab()

	iFound = False #Pixel type found

	while (not iFound):

		#Increse index/ check for the end of the grid.
		xInd += 1
		if (xInd >= 20):
			if (yInd >= 10):
				iFound = True
				break
			xInd = 0
			yInd += 1

		#Check for the pixel
		xy = (gridSize*xInd + xp, gridSize*yInd + yp)
		pixel = im.getpixel(xy)
		if CheckPixelColor(pixel, background):
			grid[yInd][xInd] = 0
			continue
		elif CheckPixelColor(pixel, safezone):
			grid[yInd][xInd] = 2
			continue
		elif CheckPixelColor(pixel, player):
			grid[yInd][xInd] = 2 #if player is found, consider it a safezone.
			continue
		elif CheckPixelColor(pixel, gridA):
			grid[yInd][xInd] = 1
			continue
		elif CheckPixelColor(pixel, gridB):
			grid[yInd][xInd] = 1
			continue
		else:
			#Checking might have found an enemy. Try again on a different screengrab
			#NOTE: DOES NOT SUPPORT YELLOW PICKUPS. Lets add that later.
			time.sleep(.1)
			im = imGrab.screenGrab()
			print("Identification faild. Re-taking screengrab. Color: " + str(pixel))

	print ("Identification finished. Result: ")
	print (grid)


def CheckPixelColor(pixel, check):
	if (pixel[0] == check[0] and pixel[1] == check[1] and pixel[2] == check[2]):
		return True
	else:
		return False


#GAME LOGIC
def LevelLoop():
	noWin = True
	#while (noWin)


def Main():
	Click(coords.startButton, "START")
	Click(coords.playGameButton, "PLAY GAME")
	#FindPlayer()
	GraphLevel()


if __name__ == '__main__':
	Main()

