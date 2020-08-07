import numpy as np
import cv2 as cv
import imutils 
import video
from common import anorm2, draw_str

#reference: https://github.com/opencv/opencv/blob/master/samples/python/lk_track.py
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, \
                  10, 0.03))

feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class App:
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(video_src)
        self.frame_idx = 0
        self.frameWidth = int(self.cam.get(3))
        self.frameHeight = int(self.cam.get(4))
        
    
    def run(self):
        color = np.random.randint(0,255,(100,3))
        out = cv.VideoWriter('result.avi', \
        cv.VideoWriter_fourcc('M','J','P','G'), 30, \
        (self.frameWidth,self.frameHeight))
        while True:
            ret, frame = self.cam.read()
            if ret==True:
                #frameNew = imutils.resize(frame, width=500)
                vis = frame.copy()
                layer = np.zeros_like(frame, dtype = "uint8")
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                
                if len(self.tracks) > 0:
                    img0, img1 = self.prev_gray, frame_gray
                    p0 = np.float32([tr[-1] for tr in self.tracks]).reshape\
                    (-1, 1, 2)
                    p1, _st, _err = cv.calcOpticalFlowPyrLK(img0, img1, p0, \
                    None, **lk_params)
                    p0r, _st, _err = cv.calcOpticalFlowPyrLK(img1, img0, p1, \
                    None, **lk_params)
                    d = abs(p0-p0r).reshape(-1, 2).max(-1)
                    good = d < 1
                    new_tracks = []
                    for tr, (x, y), good_flag in zip(self.tracks, \
                    p1.reshape(-1, 2), good):
                        if not good_flag:
                            continue
                        tr.append((x, y))
                        if len(tr) > self.track_len:
                            del tr[0]
                        new_tracks.append(tr)
                        cv.circle(layer, (x, y), 2, (255,255,255), -1)
                        cv.circle(layer, (x,y), 1, (0, 255, 0), -1)
                    self.tracks = new_tracks
                    for i in range (10):
                        cv.polylines(layer,[np.int32(tr) for tr in self.tracks]\
                        , False, color[i].tolist())
                if self.frame_idx % self.detect_interval == 0:
                    mask = np.zeros_like(frame_gray)
                    mask[:] = 255
                    for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                        cv.circle(mask, (x, y), 5, 0, -1)
                    p = cv.goodFeaturesToTrack(frame_gray, mask = mask, \
                    **feature_params)
                    if p is not None:
                        for x, y in np.float32(p).reshape(-1, 2):
                            self.tracks.append([(x, y)])
                
                self.frame_idx += 1
                self.prev_gray = frame_gray
                #out.write(layer)
                cv.imshow('Animation', layer)
                cv.imshow('Original', frame)

            ch = cv.waitKey(1)
            if ch == ord('q'):
                break
                
        self.cam.release()
        cv.destroyAllWindows()

def mainOptical(video):
    '''
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    '''
    App(video).run()
    cv.destroyAllWindows()
    print('Done')

#mainOptical('sportsclip.mov')
