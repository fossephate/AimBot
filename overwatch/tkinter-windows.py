

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

screenCenterX = screenWidth/2
screenCenterY = screenHeight/2

searchBoxX = screenCenterX - bufferX
searchBoxY = screenCenterY - bufferY

searchBoxWidth = bufferX*2
searchBoxHeight = bufferY*2


searchBoxTopLeftPointX = screenCenterX - bufferX
searchBoxTopLeftPointY = screenCenterY - bufferY

searchBoxBottomRightPointX = screenCenterX + bufferX
searchBoxBottomRightPointY = screenCenterY + bufferY




identifiedCharacters = []

targetColors = [(242,54,27), (239,53,25), (238,65,49), (237,66,51), (238,64,49), (207,135,144), (207,135,143), (217,36,17), (220,38,19), (162,77,83), (168,69,71), (178,92,98), (171,84,91)]




#root = Tk()
#root.overrideredirect(True)
#root.wait_visibility(root)

#root.wm_attributes('-alpha',0.3)
#root.wm_attributes('-topmost',True)
#root.configure(background='green')






#def pressedH(event):
    #root.destroy()
    #sys.exit()
    #print("test")

#frame = Frame(root, width=100, height=100)
#root.bind("h", pressedH)
#frame.pack()




#root.mainloop()

#place window at 50,50 and size it to 300x150
#root.geometry("300x150+50+50")
#move window to 50,50
#root.geometry("+50+50")
#sys.exit()

#while True:
    #print("test")
    #cp = win32api.GetCursorPos()
    #print (cp)
    #if win32api.GetAsyncKeyState(ord('H')):
        #print("ended program")
        #sys.exit()
        #break

'''
def moveMouse(x, y):
    program = 'moveMouse.exe'
    argument1 = str(x)
    argument2 = str(y)
    subprocess.call([program, argument1, argument2])
'''



'''
def createRectAHK(x, y, width, height):
    program = 'moveMouse.exe'
    argument1 = str(x)
    argument2 = str(y)
    subprocess.call([program, argument1, argument2])
'''

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



class MainWindow():
    counter = 0
    boxes = []
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.wait_visibility(self.root)
        
        self.root.wm_attributes('-alpha',0.1)
        self.root.wm_attributes('-topmost',True)
        self.root.configure(background='green')
        self.root.geometry("100x100+0+0")
        
        #tk.Frame.__init__(self, *args, **kwargs)
        #self.button = self.root.Button(self, text="Create new window", command=self.create_box)
        #self.button.pack(side="top")

        self.frame = Frame(self.root)

        #self.frame = Frame(self.root, width=320, height=200, borderwidth=2, relief=RAISED)
        #self.frame.pack_propagate(False)
        self.frame.pack()
        #self.createWindowButton = Button(self.frame, text="Create window", command=self.spawnBox)
        #self.createWindowButton.pack()

    def createMainBox(self, x, y, width, height):
        self.mainTopLevel = Toplevel()
        #self.mainTopLevel.overrideredirect(1)
        #self.mainTopLevel.wait_visibility(self.root)

        

        self.mainTopLevel.wm_attributes('-alpha',0.4)
        self.mainTopLevel.wm_attributes('-topmost',True)
        self.mainTopLevel.configure(background='green')

        self.mainTopLevel.geometry(str(width)+"x"+str(height)+"+"+str(x)+"+"+str(y))
        
        #self.root.configure(background='green')
        
        #self.root.geometry("50x50+300+300")

        #threading.Timer(2, self.destroyMainBox).start()

    def destroyMainBox(self):
        self.mainTopLevel.destroy()

    def moveMainBox(self, x, y):
        self.mainTopLevel.geometry("+"+str(x)+"+"+str(y))
        
    '''
    def removeABox(self):
        j = len(self.boxes)
        print(j)
        self.boxes[j].destroy()
        self.boxes.pop()

    def createBox(self, x, y, width, height):
        l = len(self.boxes)
        #self.boxes[l] = Toplevel()
        self.boxes.append(Toplevel())
        
        #self.mainTopLevel = Toplevel()
        #self.mainTopLevel.overrideredirect(1)
        #self.mainTopLevel.wait_visibility(self.root)

        self.boxes[l].configure(background='green')

        self.boxes[l].wm_attributes('-alpha',0.4)
        self.boxes[l].wm_attributes('-topmost',True)
        #self.root.configure(background='green')
        
        #self.root.geometry("50x50+300+300")

        threading.Timer(2, self.removeABox).start()
    '''


    

    def aim(self):

        if win32api.GetAsyncKeyState(ord('B')):
            self.root.destroy()
            #self.mainTopLevel.destroy()
            sys.exit()

        image = PIL.ImageGrab.grab(bbox=(searchBoxTopLeftPointX, searchBoxTopLeftPointY, searchBoxBottomRightPointX, searchBoxBottomRightPointY))
        pixels = image.load()

        for y in range(0,bufferY*2, 100):
            for x in range(0,bufferX*2, 100):
                testPixel = pixels[x,y]
                if comparePixelToPList(testPixel, targetColors, default_threshold):
                    print(testPixel)
                #print(color)

        #image.show()
        #moveMouse(100, 0)
        
        #ctypes.windll.user32.mouse_event(0x0001, 50, 0, 0, 0)
        #pyautogui.moveTo(100, 200)
        #pyautogui.moveRel(50, 0)
        #self.moveMainBox(math.floor(random.random()*1000), math.floor(random.random()*1000))
        #print("test")
        self.root.after(1500, self.aim)  # reschedule event in 2 seconds



#pyautogui.moveTo(x, y, duration=num_seconds)  # move mouse to XY coordinates over num_second seconds
#pyautogui.moveRel(xOffset, yOffset, duration=num_seconds)  # move mouse relative to its current position

#mouse = Mouse()
#mouse.move_mouse((100,0))

#MOUSEEVENTF_MOVE = 0x0001

#ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) # left down
#ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) # left up
#ctypes.windll.user32.mouse_event(0, 100, 0, 0, 0) # left down
#ctypes.windll.user32.mouse_event(0, 0, 0, 0, 0) # left up

#ctypes.windll.user32.mouse_event(0x0001, 50, 0, 0, 0)


main = MainWindow()
main.createMainBox(0, 0, 50, 100)
main.moveMainBox(20, 20)




#main.root.after(5000, test)

main.root.after(2000, main.aim)
main.root.mainloop()






