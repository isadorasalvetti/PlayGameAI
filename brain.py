import os, sys, time
import win32api, win32con
import numpy as np

import imGrab

import coords

debugMode = True

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
	on the coordinater returned by this methon.
	'''

	print("Started looking for player")

	#Find the players general area by screencaping portions of the screen and looking for red.
	found = False
	xpad, ypad = 0, 0
	itrv = 50
	while (not found):
		im = imGrab.portionGrab(itrv, itrv, xpad, ypad)
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

#GAME LOGIC
def LevelLoop():
	noWin = True
	#while (noWin)


def Main():
	Click(coords.startButton, "START")
	Click(coords.playGameButton, "PLAY GAME")
	FindPlayer()


if __name__ == '__main__':
	Main()

