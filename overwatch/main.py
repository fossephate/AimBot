

#import msvcrt
import win32api
import sys
import sched
import time
import threading
import random
import math
from tkinter import *
import pyautogui
import win32con
import ctypes
import win32gui
import subprocess
#from ctypes import *
#user32 = windll.user32
import PIL


screenWidth, screenHeight = pyautogui.size()

bufferX = 300
bufferY = 300

screenCenterX = screenWidth
screenCenterY = screenHeight

searchBoxWidth = bufferX*2
searchBoxHeight = bufferY*2


searchBoxTopLeftPointX = screenCenterX - bufferX
searchBoxTopLeftPointY = screenCenterY - bufferY

searchBoxBottomRightPointX = screenCenterX + bufferX
searchBoxBottomRightPointY = screenCenterY + bufferY




identifiedCharacters = []

targetColors = [(242,54,27), (239,53,25), (238,65,49), (237,66,51), (238,64,49), (207,135,144), (207,135,143), (217,36,17), (220,38,19), (162,77,83), (168,69,71), (178,92,98), (171,84,91)]




'''
def moveMouse(x, y):
    program = 'moveMouse.exe'
    argument1 = str(x)
    argument2 = str(y)
    subprocess.call([program, argument1, argument2])
'''




def createRectAHK(x, y, width, height, center):

    if center:
        x = x - (width/2)
        y = y - (height/2)
    width = width/2
    height = height/2
    
    
    program = 'createRect.exe'
    arg1 = str(x)
    arg2 = str(y)
    arg3 = str(width)
    arg4 = str(height)
    
    subprocess.call([program, arg1, arg2, arg3, arg4])


'''
px=ImageGrab.grab().load()
for y in range(0,100,10):
    for x in range(0,100,10):
        color=px[x,y]
'''


default_threshold = 18

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold

def comparePixelToPList(pixel, pList, threshold):
    for i in range(0, len(pList)):
        cPixel = pList[i]
        if is_similar(pixel, cPixel, threshold):
            return True
    return False





def loop():
    while(True):
        if win32api.GetAsyncKeyState(ord('B')):
            sys.exit()

        SBTLPX = searchBoxTopLeftPointX
        SBTLPY = searchBoxTopLeftPointY

        SBBRPX = searchBoxBottomRightPointX
        SBBRPY = searchBoxBottomRightPointY

        #print(Sc

        #createRectAHK(screenCenterX, screenCenterY, 10, 10, True)
        
        #createRectAHK(SBTLPX, SBTLPY, 100, 100, True)
        #createRectAHK(SBBRPX, SBBRPY, 100, 100, True)

        createRectAHK(SBTLPX, SBTLPY, bufferX*2, bufferY*2, False)

        #createRectAHK(0, 0, 1500, 1000, False)
        #createRectAHK(1500, 1000, 1500, 1000, True)

        image = PIL.ImageGrab.grab(bbox=(SBTLPX, SBTLPY, SBBRPX+bufferX, SBBRPY+bufferY))
        pixels = image.load()
        

        for y in range(0, bufferY*2, 50):
            for x in range(0, bufferX*2, 50):
                testPixel = pixels[x, y]

                #actualX = searchBoxTopLeftPointX + x
                #actualY = searchBoxTopLeftPointY + y
                
                #pyautogui.moveTo(actualX, actualY)
                if comparePixelToPList(testPixel, targetColors, default_threshold):
                    print(x)
                    actualX = searchBoxTopLeftPointX + x
                    actualY = searchBoxTopLeftPointY + y
                    #print(actualX)
                    createRectAHK(actualX, actualY, 25, 25, True)
                    #print(testPixel)



#pyautogui.moveTo(x, y, duration=num_seconds)  # move mouse to XY coordinates over num_second seconds

#createRectAHK(0, 0, 100, 100)
loop()




