from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from PIL import Image
import pyautogui
#import subprocess
import ctypes
from ctypes import *
import win32api
import win32con
import win32com
import win32com.client
import win32gui
import win32ui
import time



screenWidth, screenHeight = pyautogui.size()

def RGB2HSV(R, G, B):
        color = np.uint8([[[B, G, R]]])
        hsvc = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
        hsv = (hsvc[0][0][0], hsvc[0][0][1], hsvc[0][0][2])
        print(hsv)
        return (hsv[0], hsv[1], hsv[2])


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

def moveMouseRel(xOffset, yOffset):
        ctypes.windll.user32.mouse_event(0x0001, xOffset, yOffset, 0, 0)



# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
        help="max buffer size")
args = vars(ap.parse_args())


# define the lower and upper boundaries of the color
# in the HSV color space
#lw = RGB2HSV(148, 159, 0)
#up = RGB2HSV(244, 249, 170)
#colorLower = ( int(lw[0]) , int(lw[1]), int(lw[2]) )
#colorUpper = ( int(up[0]) , int(up[1]), int(up[2]) )
#colorMiddle = RGB2HSV(223, 239, 0)


# In HSV:
#colorLower = (120, 90, 25)
#colorUpper = (122, 200, 200)
colorLower = np.array([115,100,120])
colorUpper = np.array([130,255,255])

#colorLower = np.array([120, 80, 80],np.uint8)
#colorUpper = np.array([130, 255, 255],np.uint8)




# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""


bufferX = 250
bufferY = 100
centerX = screenWidth/2
centerY = screenHeight/2

x1 = centerX - bufferX
y1 = centerY - bufferY

x2 = centerX + bufferX
y2 = centerY + bufferY

w = bufferX*2
h = bufferY*2



#get window position and info
hwnd = win32gui.FindWindow(None, "Overwatch")
#hwnd = win32gui.GetDesktopWindow()#for screenshot of entire screen
l, t, r, b = win32gui.GetWindowRect(hwnd)
windowHeight = b-t
windowWidth = r-l
windowCenterX = windowWidth/2
windowCenterY = windowHeight/2


SSx1 = int(windowCenterX - bufferX)
SSy1 = int(windowCenterY - bufferY)
SSWidth = bufferX*2
SSHeight = bufferY*2


toggle = False
timeSinceLastToggle = time.clock()


# loop
while (1):
        
        start = time.clock()

        # give overwatch focus
        #shell=win32com.client.Dispatch("Wscript.Shell")
        #success = shell.AppActivate("Overwatch") # Returns true if focus given successfully.
        
        #get window position and info
        hwnd = win32gui.FindWindow(None, "Overwatch")
        #hwnd = win32gui.GetDesktopWindow()#for screenshot of entire screen
        
        wDC = win32gui.GetWindowDC(hwnd)
        myDC = win32ui.CreateDCFromHandle(wDC)
        newDC = myDC.CreateCompatibleDC()
        myBitMap = win32ui.CreateBitmap()
        myBitMap.CreateCompatibleBitmap(myDC, w, h)
        newDC.SelectObject(myBitMap)
        newDC.BitBlt((0,0),(SSWidth, SSHeight) , myDC, (SSx1,SSy1), win32con.SRCCOPY)

        bmpinfo = myBitMap.GetInfo()
        bmpstr = myBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # Free Resources
        myDC.DeleteDC()
        newDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(myBitMap.GetHandle())
        
        #img = ImageGrab.grab(bbox=(x1, y1, x2, y2))#.crop(box) #x, y, w, h
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        #frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)

        
        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        #mask = cv2.dilate(mask, None, iterations=1)
        #mask = cv2.erode(mask, None, iterations=1)
        #mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        #contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
        center = None

        
        #cv2.drawContours(frame, contours, -1, (0,255,255), 5)

        # only proceed if at least one contour was found
        if len(contours) > 0:
                
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                contour = max(contours, key=cv2.contourArea)
                #draw the largest contour
                cv2.drawContours(frame, [contour], 0, (128,255,0), 2, maxLevel = 0)

                
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                #center = (int(x),int(y))
                #radius = int(radius)
                #cv2.circle(frame,center,radius,(0,255,0),2)
                
                
                if(radius > 20):
                        M = cv2.moments(contour)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        pts.appendleft(center)

                '''
                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        pts.appendleft(center)
                '''

                '''
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame,[box],0,(0,0,255),2)
                '''
                        
        '''
        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        pts.appendleft(center)
        '''

        '''
        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                        continue
                # check to see if enough points have been accumulated in
                # the buffer
                #if counter >= 10 and i == 1 and pts[-10] is not None:
                if counter >= 10 and i == 1 and len(pts) >= 10:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction
                        # text variables
                        dX = pts[-10][0] - pts[i][0]
                        dY = pts[-10][1] - pts[i][1]
                        (dirX, dirY) = ("", "")
                        # ensure there is significant movement in the
                        # x-direction
                        if np.abs(dX) > 20:
                                dirX = "East" if np.sign(dX) == 1 else "West"
                        # ensure there is significant movement in the
                        # y-direction
                        if np.abs(dY) > 20:
                                dirY = "North" if np.sign(dY) == 1 else "South"
                        # handle when both directions are non-empty
                        if dirX != "" and dirY != "":
                                direction = "{}-{}".format(dirY, dirX)
                        # otherwise, only one direction is non-empty
                        else:
                                direction = dirX if dirX != "" else dirY
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        '''
                
        cv2.putText(frame, str(counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
        counter += 1

        # show screen capture and mask
        cv2.imshow("screen capture", frame)
        cv2.imshow("mask", mask)
        
        xSpdMod = 0.1
        ySpdMod = 0.1
        spd = 20


        if(center != None):
                targetX = center[0]+x1
                targetY = center[1]+y1
                xDistance = centerX - targetX
                yDistance = centerY - targetY

                '''xDistances.append(xDistance)
                if(len(xDistances) > 5):
                        l = len(xDistances)
                        if(abs(xDistances[l-1]) > abs(xDistances[l-2])):
                                xSpdMod += 0.001
                                '''
                
                            
                xSpd = xDistance*xSpdMod
                ySpd = yDistance*ySpdMod

                if toggle:
                        moveMouseRel(int(-xSpd), 0)
                        if(ySpd > 0):
                                moveMouseRel(0, int(-ySpd))

                        #moveMouseRel(int(-xSpd), 0)
                        #moveMouseRel(0, int(-ySpd))
        




        
        cv2.waitKey(10)

        # global quit
        if win32api.GetAsyncKeyState(ord('U')):
                break
        
        if win32api.GetAsyncKeyState(ord('G')):
                diff = time.clock() - timeSinceLastToggle
                if(diff > 0.5):
                        timeSinceLastToggle = time.clock()
                        toggle = not toggle
        
        '''
        key = cv2.waitKey(1)
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break
        '''
        
        end = time.clock()
        
        diffInSeconds = end - start
        diffInMilliSeconds = diffInSeconds*1000
        FPS = 1000 / diffInMilliSeconds
        #print(diffInMilliSeconds)
        

# close any open windows
cv2.destroyAllWindows()
