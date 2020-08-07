import numpy as np
import cv2
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import imutils 
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import time
#from menuewindow import mfileopen

#code reference: https://buildmedia.readthedocs.org/media/pdf/opencv24-python-tutorials/stable/opencv24-python-tutorials.pdf 
def opticalFlow(video):
    #optical flow
    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                        qualityLevel = 0.3,
                        minDistance = 7,
                        blockSize = 7 )
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,\
                10, 0.03))
    
    color = np.random.randint(0,255,(100,3)) #create random colors 
    
    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    #frameNew = imutils.resize(old_frame, width=500)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    #use ShiTomasi Corner detection to track corners in original frame 
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    
    # Create a mask image for drawing
    mask = np.zeros_like(old_frame, dtype = "uint8")
    out = cv2.VideoWriter('result.avi', \
    cv2.VideoWriter_fourcc('M','J','P','G'),30, (frame_width,frame_height))
    
    while(1):
        ret,frame = cap.read()
        
        if ret == True:
            #frameNew = imutils.resize(frame, width=500)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, \
            None, **lk_params)
            if p1 is None:
                p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, \
                **feature_params)
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, \
                frame_gray, p0, None, **lk_params)
            # Select good points
            good_new = p1[st==1]
            good_old = p0[st==1]
        
            # draw tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2) 
                draw = cv2.circle(mask,(a,b),3,color[i].tolist(),-1)
                draw = cv2.circle(mask,(a,b),1,color[i].tolist(),-1)
                
            new = cv2.add(draw, mask)
            frame2 = frame.copy()
            
            out.write(new)
            #cv2.imshow('Original',frameNew)
            #cv2.imshow('Animation',new)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q'):
                break
                
        else:
            break 
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)
    
    cap.release()
    cv2.destroyAllWindows()
    

    for i in range (1,5):
        cv2.waitKey(0)

#opticalFlow('diving.avi')

def denseFlow(video):

#dense optical flow
    #take a video input
    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    #convert the first frame into gray 
    ret, frame1 = cap.read()
    prev = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    out = cv2.VideoWriter('result.avi', \
    cv2.VideoWriter_fourcc('M','J','P','G'),60, (frame_width,frame_height))
    #create the HSV color image 
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    
    while(1):
        ret, frame2 = cap.read()
        if ret == True:
            next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev, next, None, \
            0.5, 3, 15, 3, 5, 1.2, 0)
            #flow magnitude and direction angle 
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            #update the color image 
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        
            frame3 = frame2.copy()
            out.write(rgb)
            #cv2.imshow('Animation',rgb)
            #cv2.imshow("original", frame3)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q'):
                break
            elif k==ord('s'):
                cv2.imshow("animation", )
            
        else:
            break 
    
    cap.release()
    cv2.destroyAllWindows()
    

#denseFlow("fish1.avi")