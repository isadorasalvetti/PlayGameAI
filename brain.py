import os, sys, time
import win32api, win32con
import coords

debugMode = True

def Click(buttonCoord, func=""):
	win32api.SetCursorPos(buttonCoord)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(.1)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	if (debugMode):
		print ("Click " + func)

def FindPlayer():
	'''
	FIND THE PLAYER
	To be run at the start of every level. Further movement will depend
	on the coordinater returned by this methon.
	'''

def LevelLoop():
	noWin = True
	while (noWin)


def Main():
	Click(coords.startButton, "START")
	Click(coords.playGameButton, "PLAY GAME")

if __name__ == '__main__':
	Main()

