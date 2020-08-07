import cv2 as cv
########algorithm of opticalFlow#############
import numpy as np
from scipy import signal
def optical_flow(I1g, I2g, window_size, tau=1e-2):
 
    kernel_x = np.array([[-1., 1.], [-1., 1.]])
    kernel_y = np.array([[-1., -1.], [1., 1.]])
    kernel_t = np.array([[1., 1.], [1., 1.]])#*.25
# window_size is odd, all the pixels with offset in between [-w, w] are inside the window
    w = window_size/2 
    I1g = I1g / 255. # normalize pixels
    I2g = I2g / 255. # normalize pixels
    # Implement Lucas Kanade
    # for each point, calculate I_x, I_y, I_t
    mode = 'same'
    fx = signal.convolve2d(I1g, kernel_x, boundary='symm', mode=mode)
    fy = signal.convolve2d(I1g, kernel_y, boundary='symm', mode=mode)
    ft = signal.convolve2d(I2g, kernel_t, boundary='symm', mode=mode) + \
    signal.convolve2d(I1g, -kernel_t, boundary='symm', mode=mode)
    u = np.zeros(I1g.shape)
    v = np.zeros(I1g.shape)
    # within window window_size * window_size
    for i in range(w, I1g.shape[0]-w):
        for j in range(w, I1g.shape[1]-w):
            Ix = fx[i-w:i+w+1, j-w:j+w+1].flatten()
            Iy = fy[i-w:i+w+1, j-w:j+w+1].flatten()
            It = ft[i-w:i+w+1, j-w:j+w+1].flatten()
            #b = ... # get b here
            #A = ... # get A here
            # if threshold τ is larger than the smallest eigenvalue of A'A:
            nu = ... # get velocity here
            u[i,j]=nu[0]


#code reference: https://github.com/opencv/opencv/blob/master/samples/python/opt_flow.py 
# Python 2/3 compatibility



def draw_flow(img, flow, step=8):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    #print(fx, fy)
    lines = np.vstack([x,y,x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.polylines(vis, lines, 0, (255,165,0))#(0, 255, 0))
    for (x1, y1), (_x2, _y2) in lines:
        cv.circle(vis, (x1, y1), 1, (0, 0, 0), -1)
    return vis


def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return bgr


def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv.remap(img, flow, None, cv.INTER_LINEAR)
    return res 

def main(video):
    import sys
    '''
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 0
    '''
    cam = cv.VideoCapture(video)
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    ret, prev = cam.read()
    prevgray = cv.cvtColor(prev, cv.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()
    out = cv.VideoWriter('result.avi', cv.VideoWriter_fourcc('M','J','P','G'), \
    60, (frame_width,frame_height))
    mask = np.zeros_like(prevgray, dtype = "uint8")
    while True:
        ret, img = cam.read()
        if ret:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, \
            pyr_scale = 0.5, levels = 3, winsize = 15, iterations = 3, \
            poly_n = 5, poly_sigma = 1.2, flags = 0)
            prevgray = gray
            cv.imshow("Original", img)
            showFrame = gray.copy()
            cv.imshow('Animation', draw_flow(mask, flow))
            #cv.imshow("Animation", draw_flow(gray, flow))            
            #out.write(draw_flow(mask, flow))
        
            if show_hsv:
                cv.imshow('flow HSV', draw_hsv(flow))
            if show_glitch:
                cur_glitch = warp_flow(cur_glitch, flow)
                cv.imshow('glitch', cur_glitch)
        
        ch = cv.waitKey(1)
        if ch == ord('q'):
            break
        
        if ch == ord('1'):
            show_hsv = not show_hsv
            print('HSV flow visualization is', ['off', 'on'][show_hsv])
        if ch == ord('2'):
            show_glitch = not show_glitch
            if show_glitch:
                cur_glitch = img.copy()
            print('glitch is', ['off', 'on'][show_glitch])
        
    cam.release()
    cv.destroyAllWindows()
    print('Done')

#main('outpy.avi')



