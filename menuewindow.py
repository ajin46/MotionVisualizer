#starter code from 112 website 

from tkinter import *
import cv2
from PIL import ImageTk, Image
import os,sys,time
import numpy as np
from tkinter import ttk
from tkinter import filedialog
from OpticalFlow import*
from opticalFlowAlg import*
from opticalFlowNew import*
import imageio
####################################
#liveCam
####################################
#reference: https://www.youtube.com/watch?v=BDt0-F3PL8U
def liveCam():
    # init camera
    camera = cv2.VideoCapture(0)
    camera.set(3,320)
    camera.set(4,240)
    
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M','J','P','G'),\
    30, (frame_width,frame_height))
    
    while 1:
        # grab a frame
        (ret,frame) = camera.read()
        
        if ret==True:
            frame = cv2.flip(frame, 1) 
            out.write(frame)
            cv2.imshow("Recording",frame)
            key = cv2.waitKey(60) & 0xFF
            if key == ord('e'):
                break
            elif key != 255:
                print('key:',[chr(key)])
        # end of feed
        else:
            break
        
        # key delay and action
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key != 255:
            print('key:',[chr(key)])
    # release camera
    camera.release()
    out.release()
    # close all windows
    cv2.destroyAllWindows()


#upload Function 

def showVideo(original):
    cap = cv2.VideoCapture(original)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    while(1):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Original',frame)
        else:
            break 
            
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
    cap.release()
    #cv2.destroyAllWindows()
    

def showNew(new):
    cap = cv2.VideoCapture(new)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    while(1):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Animation',frame)
        else:
            break 
            
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
    cap.release()
    #cv2.destroyAllWindows()
    

def showBoth(original, new):
    capOld = cv2.VideoCapture(original)
    capNew = cv2.VideoCapture(new)
    while(1):
        retOld, frameOld = capOld.read()
        retNew, frameNew = capNew.read()
        if (retOld and retNew) == True:
            cv2.imshow('Original',frameOld)
            cv2.imshow('Animation',frameNew)
        else:
            break 
            
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
    capOld.release()
    capNew.release()
    cv2.destroyAllWindows()
    

####################################
# customize these functions
####################################
#code reference: 112 website 
def init(data):
    data.mode = "startWindow"
    loadImages(data)
    loadImageIns(data)
    loadImageUp(data)
    data.MotionPos = (0,0)
    data.MotionPosn = (0,0)
    

def mousePressed(event, data):
    if (data.mode == "startWindow"): startWindowMousePressed(event, data)
    elif (data.mode == 'instructionPage'): instructionMousePressed(event, data)
    elif (data.mode == "uploadWindow"): uploadWindowMousePressed(event, data)
    

def keyPressed(event, data):
    if (data.mode == "startWindow"): startWindowKeyPressed(event, data)
    elif (data.mode == 'instructionPage'): instructionKeyPressed(event, data)
    elif (data.mode == "uploadWindow"): uploadWindowMousePressed(event, data)
    

def redrawAll(canvas, data):
    if (data.mode == "startWindow"): startWindowRedrawAll(canvas, data)
    elif(data.mode == 'process'): processPage(canvas, data)
    elif (data.mode == 'instructionPage'): instructionRedrawAll(canvas, data)
    elif (data.mode == "uploadWindow"): uploadWindowRedrawAll(canvas, data)
    
####################################
#start Window Mode
####################################


def mouseMotion(event,data):
    data.MotionPos = (event.x, event.y)
    
def loadImages(data):
    data.photo = PhotoImage(file = 'Motion.png')

def startWindowMousePressed(event, data):
    if (event.x > data.width//2 - data.width//15 and\
        event.x < data.width//2 + data.width//15 and\
        event.y > 3*data.height//4 - data.height//30 and\
        event.y < 3*data.height//4 + data.height//30):
        data.mode = "instructionPage"

def startWindowKeyPressed(event, data):
    pass 

def startWindowTimerFired(data):
    pass
   
def startWindowRedrawAll(canvas, data):
    cx = data.width//2
    cy = 3*data.height//4
    recWidth = data.width//15
    recHeight = data.height//30
    #canvas.create_rectangle(0,0,data.width, data.height, fill='lightcyan')
    canvas.create_rectangle(cx - recWidth, cy- recHeight, cx + recWidth, cy + \
    recHeight, outline='midnightblue', width = 5)
    canvas.create_text(cx, cy, text = "Start", font="Times 28 bold italic", \
    fill='midnightblue')
    
    canvas.create_image(data.width//2, data.height//2, anchor = S, \
    image=data.photo)
    (x,y) = data.MotionPos
    r = 5
    canvas.create_oval(x-r, y-r, x+r, y+r, fill='indigo')
    canvas.create_oval(x+r, y+r, x+2*r, y+2*r, fill = 'indigo')


####################################
#Instruction Page 
####################################

def loadImageIns(data):
    data.photo1 = PhotoImage(file = 'Instruction.png')
    data.photo2 = PhotoImage(file = 'Ins1.png')
    data.photo3 = PhotoImage(file = 'Ins2.png')
    data.photo4 = PhotoImage(file = 'Ins3.png')
    data.photo5 = PhotoImage(file = 'Ins4.png')
    
def mouseMotion2(event,data):
    data.MotionPosn = (event.x, event.y)
    
def instructionKeyPressed(event, data):
    pass 

def instructionMousePressed(event, data):
    if event.x > 5*data.width//6 - data.width//15  and\
       event.x < 5*data.width//6 + data.width//15 and\
       event.y > 5*data.height//6-data.height//30 and\
       event.y < 5*data.height//6 + data.height//30:
        data.mode = 'uploadWindow'

def instructionRedrawAll(canvas, data):
    cx = data.width//2
    cy = data.height//2
    canvas.create_image(cx, cy-cy//1.3, anchor = S, image=data.photo1)
    canvas.create_image(cx , cy//2, anchor = S, image = data.photo2)
    canvas.create_image(cx  + 20, cy - cy//4.5, anchor = S, image = data.photo3)
    canvas.create_image(cx + 40, cy - cy//10, image = data.photo4)
    canvas. create_image(cx-190, cy + 25 , image = data.photo5)
    canvas.create_rectangle(5*data.width//6 - data.width//15 , \
    5*data.height//6-data.height//30, \
    5*data.width//6 + data.width//15 , 5*data.height//6 + data.height//30, outline='midnightblue', width = 5)
    canvas.create_text(5*data.width//6, 5*data.height//6, text = 'Next', \
    font="Times 28 bold italic", fill = 'midnightblue')
    (x,y) = data.MotionPosn
    r = 5
    canvas.create_oval(x-r, y-r, x+r, y+r, fill='indigo')
    canvas.create_oval(x+r, y+r, x+2*r, y+2*r, fill = 'indigo')
    
    
    
####################################
#Upload Window Mode
####################################
def processPage(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill='lightcyan')
    canvas.create_text(data.width//2, data.height//2, text='Done!')

def loadImageUp(data):
    data.photo6 = PhotoImage(file = 'Up.png')
    data.photo7 = PhotoImage(file = 'Up1.png')
    data.photo8 = PhotoImage(file = 'Up2.png')
    data.photo9 = PhotoImage(file = 'mode1.png')
    data.photo10 = PhotoImage(file = 'mode2.png')
    data.photo11 = PhotoImage(file = 'mode3.png')
    data.photo12 = PhotoImage(file = 'mode4.png')
    data.photo13 = PhotoImage(file = 'Up3.png')
    data.photo14 = PhotoImage(file = 'Up4.png')

def mcolor():
    color = colorchooser.askcolor()
    label = Label(text="your choosen color", bg = color[1]).pack()

def mfileopen():
    file1 = filedialog.askopenfile()
    if file1:
        print(((file1.name).split('/')[-1]))
        return ((file1.name).split('/')[-1])
    else:
        return None 
        
def uploadWindowMousePressed(event, data):
    cx1 = data.width//2.5
    cy1 = 3*data.height//4
    cx2 = data.width//3 + 20
    cy2 = data.height//2.2
    recW = data.width//20 
    recH = data.height//30
    cx3 = data.width //2
    cy3 = data.height//2
    #data.mode = 'process'
    #liveCam
    if event.x > (data.width//2-recW) and \
        event.x < (data.width//2+recW) and \
        event.y > (data.height//2.2 - recH) and \
        event.y < (data.height//2.2 + recH):
        liveCam()
            
    #optical Flow 
    elif event.x > (data.width//5 - 15) and \
            event.x < (data.width//5 + 15) and \
            event.y > 2.1*(data.height//3) - 15 and \
            event.y < 2.1*(data.height//3) + 15:
            path = mfileopen()
            opticalFlow(path)
            showBoth(path, 'result.avi')
                
                
    #dense optical flow 
    elif event.x > 2*(data.width//5) - 15 and \
            event.x < 2*(data.width//5) + 15 and \
            event.y > 2.1*(data.height//3) - 15 and \
            event.y <  2.1*(data.height//3) + 15:
            path = mfileopen()
            denseFlow(path)
            showBoth(path, 'result.avi')
    
    #opticalFlow Accurate 
    elif event.x > 3*(data.width//5) - 15 and \
            event.x < 3*(data.width//5) + 15 and \
            event.y > 2.1*(data.height//3) - 15 and \
            event.y < 2.1*(data.height//3) + 15:
            path = mfileopen()
            mainOptical(path)
            showBoth(path, 'result.avi')
            
    #opticalFlow slow blue 
    elif event.x > 4*(data.width//5) - 15 and \
            event.x < 4*(data.width//5) + 15 and \
            event.y >  2.1*(data.height//3) - 15 and \
            event.y < 2.1*(data.height//3) + 15:
            path = mfileopen()
            main(path)
            showBoth(path, 'result.avi')
            

def uploadWindowKeyPressed(event, data):
    pass 

def uploadWindowTimerFired(data):
    pass

def uploadWindowRedrawAll(canvas, data):
    cx1 = data.width//2.5
    cy1 = 3*data.height//4
    cx2 = data.width//3 + 20
    cy2 = data.height//2.2
    recW = data.width//20 
    recH = data.height//30
    cx3 = data.width //2
    cy3 = data.height//2
    r = 20
    #title 
    canvas.create_image(data.width//2, data.height//6, image=data.photo6)
    canvas.create_image(data.width//2, data.height//3, image = data.photo7)
    canvas.create_image(data.width//2, data.height//2+ 50, image = data.photo8)
    canvas.create_image(data.width//2, data.height//3 + 40, \
    image = data.photo13)
    canvas.create_image(data.width//2, data.height//2+ 90, image = data.photo14)
    #liveCam button 
    canvas.create_rectangle(data.width//2-recW, cy2- recH, data.width//2 + \
    recW, cy2 + recH, outline='purple', width = 0, fill = 'lavender')
    canvas.create_text(data.width//2, cy2, text = "LiveCam", \
    font="Times 20 bold italic", fill = 'purple')
    
    #opticalFlow
    canvas.create_image(data.width//5, 2.1*(data.height//3), \
    image = data.photo9)
    
    #opticalDenseFLow 
    canvas.create_image(2*(data.width//5), 2.1*(data.height//3), \
    image = data.photo10)
    
    #newOptical FLOW
    canvas.create_image(3*(data.width//5), 2.1*(data.height//3), \
    image = data.photo11)
    
    #advanced opticalflow 
    canvas.create_image(4*(data.width//5), 2.1*(data.height//3), \
    image = data.photo12)
    

####################################
# use the run function as-is
####################################
#code from 112 website 
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseMotionWrapper(event, canvas, data):
        mouseMotion(event, data)
        mouseMotion2(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event: 
                            mouseMotionWrapper(event, canvas, data))
    redrawAllWrapper(canvas, data)
    # and launch the app
    root.mainloop() # blocks until window is closed
    print("bye!")
    

run(800, 800)