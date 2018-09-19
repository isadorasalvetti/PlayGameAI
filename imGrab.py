from PIL import ImageGrab
from PIL import ImageOps
import os
import time
 
'''
Grab a snapshot of the current area.

'''

# GLOBALS:

# Image sizing
xPad = 0
yPad = 105
xEnd = 996
yEnd = 742

def screenGrab():
	box = (xPad + 1, yPad + 1, xPad + xEnd, yPad + yEnd)
	im = ImageGrab.grab(box) # Returns RBG image
	#im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG') # Saves RBG image as full_snap__TIME.png
	return im

def portionGrab(xsize, ysize, xpad, ypad):
	box = (xPad + xpad, yPad + ypad, xPad + xpad + xsize, yPad + ypad + ysize)
	im = ImageGrab.grab(box)
	#im.save(os.getcwd() + '\\part_snap__' + str(int(time.time())) + '.png', 'PNG') # Saves RBG image as full_snap__TIME.png
	return im

def saveIm(im):
	im.save(os.getcwd() + '\\part_snap__' + str(int(time.time())) + '.png', 'PNG') # Saves RBG image as full_snap__TIME.png
	
def main():
    screenGrab()
 
 # Does a screengrab on execution.
if __name__ == '__main__':
    main()