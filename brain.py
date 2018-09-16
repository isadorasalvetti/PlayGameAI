import os, sys, time
import win32api, win32con
from PIL import ImageGrab
from PIL import ImageOps
import numpy as np
import queue

import imGrab

import coords

debugMode = True

#PLAYER INFO
playerSize = 36 # Square
playerBorder =  6 # Border thickness

#ENVIRONMENT INFO
maxDist = 799
headerSizeY = 100 #Only black = 70. Extra pixels added to fit the grid better,
gridSize = 50
gameSize = (11, 20)

minEnemySize = 18 #Minimun interval size to check for enemies 

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

def MoveRight():
	win32api.keybd_event(coords.VK_CODE[right_arrow], 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(coords.VK_CODE[right_arrow], 0 ,win32con.KEYEVENTF_KEYUP ,0)

#VISION UTILITIES
def CheckPixelColor(pixel, check):
	if (pixel[0] == check[0] and pixel[1] == check[1] and pixel[2] == check[2]):
		return True
	else:
		return False

def LookForEnemy(pixel):
	if (pixel[1] < 100):
		return maxDist
	else:
		return 100

#GRAPH
class LevelGraph:

	'''
	Store LEVEL INFORMATION - level design, player initial position, 
	objective position.

	'''

	def __init__(self):
		self.initPos = (0, 0) #initial position of the player IN GRAPH.
		self.endPos =[]
		self.graph = self.GraphLevel()
		self.playerCoords = self.FindPlayer()
		self.objectiveCoords = []
		self.PathFinding() #Finds path/ list of objectives for the player.
		print ("Level Finished. Result: ")
		print (self.graph)

	def FindPlayer(self): #CHECKED, working
		
		'''
		FIND THE PLAYER
		To be run at the start of every level. Further movement will depend
		on the coordinates returned by this method.
		'''

		print("")
		print("Started looking for player")

		#Find the players general area by screencaping portions of the screen and looking for red.
		#TODO: This process is slow and probably unecessary. Replace by a more general pixel by pixel lookup and remove this section.
		#------ Look in intervals of PLAYERSIZE. 
		#------ Start search from middle of the scren and expand toward the corners.
		found = False
		playerPos = (0, 0)
		xpad, ypad = 0, headerSizeY
		itrv = gridSize
		while (not found):
			img = imGrab.portionGrab(itrv, itrv, xpad, ypad)
			im = img.getcolors()
			for i in im:
				if (i[1][0] == 255 and i[1][1] == 0 and i[1][2] == 0):
					print(str(i[1][0]) + ", " + str(i[1][1]) + ", " + str(i[1][2]))
					found = True
					if (debugMode):
						print("Character found in quadrant " + str(xpad/itrv) +", "+ str(ypad/itrv))
						self.initPos = (int(xpad/itrv), int(ypad/itrv))
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

	def GraphLevel(self): #works... for the most part. Needs review.

		'''
		FIND the SHAPE of the level.
		To be used for path finding.

		'''

		print("")
		print("Started creating level grid.")

		grid = np.zeros(gameSize, int)
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
				#Checking might have found an enemy/ moving obstacle. Try again on a different screengrab
				#TODO: DOES NOT SUPPORT YELLOW PICKUPS. Lets add that later.
				time.sleep(.2)
				im = imGrab.screenGrab()
				print("Identification faild. Re-taking screengrab. Color: " + str(pixel))

		#TODO: a few nodes fail. Verify why.
		return grid

	def FindClusters(self): #UNFINISHED! TODO
		'''
		Find the green clusters in the graph.
		Save points/ objective point.

		'''

		initNode = self.initPos
		availableConnections = getNeighboors(self.graph, initNode)

		for node in availableConnections:
			if (node == 0):
				print("to b cont...")

	def PathFinding(graph, start, target): #INCOMPLETE
		'''
		Find the best path to the end of the level.
		Returns list of key nodes to be visited.
		The bot will base its movements on this list.

		

		frontier = queue.Queue()
		frontier = put(start) #Initialize frontier with only start position
		visited = np.zeros(gameSize, bool) #Initialize visited list
		cost = np.zeros((11, 20), bool) #Initialize list of node costs
		visited[start[0]][start[1]] = True

		while not frontier.empty():
			current = frontier.get()
			for next in graph.neighbors(current):
				if not visited[next[0]][next[1]]:
					frontier.put(next)
					'''
		
		nodes = [(10, 4), (10, 6), (4, 13), (4, 15)]
		for n in nodes:
			coord = (n[0]*gridSize, n[1]*gridSize)
			self.objectiveCoords.append(coord)
		print ("New path found! -not working")

	def getNextObjective():
		#Removes and returns next member from the list of objective coordinates
		coords = self.objectiveCoords.pop(0)
		return coords

def getNeighboors(graph, node): #UNTESTED, currently not in use.
	'''
	Returns a list of indices of the bottom, up,
	right and left nodes to the one passed

	'''

	xDim = len(graph[0])-1
	yDim = len(graph)-1
	left = (node[0], min(max(0,(node[1]-1)), xDim))
	right = (node[0], min(max(0,(node[1]+1)), xDim))
	up = (min(max(0,node[0]+1), yDim), node[1])
	down = (min(max(0,node[0]-1), yDim), node[1])

	return (left, right, up, down)

#DONT DIE
def MoveToObjective(level):
	'''
	Move the player.
	Cost of each direction = distance from the next objective node.
	If an enemy is found in that direction - cost is infinite.	

	'''

	while (len(level.objectiveCoords) > 0): #Repeat while there are still objectives to go to
		#Grab image around player
		playerPos = (level.playerCoords[0], level.playerCoords[1]) # (x, y)
		sampleSize = 150
		xpad, ypad = playerPos[0] + playerSize/2 - sampleSize/2, playerPos[1] + playerSize/2 - sampleSize/2
		img = imGrab.portionGrab(sampleSize, sampleSize, xpad, ypad)
		
		#Find the next objective to move to
		nextObjective = level.getNextObjective()
		print("Attempting to move towards " + str(nextObjective))

		objectiveReached = False
		while not objectiveReached:
			rgt = calcCost(img, sampleSize, coords.right, objective)


def calcCost(img, sampleSize, dir, obj):
	'''
	Calculates the cost of moving into a direction.

	'''
	center = sampleSize/2
	nSamples = (sampleSize/2 -playerSize/2) / minEnemySize

	#Taking samples of the area in the chosen direction
	for smplN in range (nSamples):
		smpl = smpl + minEnemySize
		xy = (smpl*dir[0], smpl*dir[1])
		pixel = im.getpixel(xy)
		LookforEnemy(pixel)

	return cost

def Main():
	#Click(coords.startButton, "START")
	#Click(coords.playGameButton, "PLAY GAME")
	level = LevelGraph()
	MoveToObjective(level)


if __name__ == '__main__':
	Main()

