from PIL import ImageGrab
import os
import time
 
'''
Grab a snapshot of the current area.

'''

# GLOBALS:

# Image sizing
xPad = 98
yPad = 105
xEnd = 996
yEnd = 742

def screenGrab():
    box = (xPad + 1, yPad + 1, xPad + xEnd, yPad + yEnd)
    im = ImageGrab.grab(box) # Returns RBG image
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG') # Saves RBG image as full_snap__TIME.png
 
def main():
    screenGrab()
 
 # Does a screengrab on execution.
if __name__ == '__main__':
    main()