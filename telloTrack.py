# This file adds onto the tutorial track file found in  the archive
# this file tracks using the video stream from the tello

# import the necessary packages
from collections import deque
from helpers import *
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

from djitellopy import Tello

debug = False

# cmd line args parse: construct the argument parse and parse the arguments
# video input set up here
# buffer of deque obj (line follower or "contrail")
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "blue"
# ball in the HSV color space, then initialize the
# list of tracked points
blueLower = (97, 105, 103)
blueUpper = (112, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the tello
telloStream = not args.get("video", False)
if telloStream:
    tello = Tello()
    tello.connect()
    tello.streamon()

    if not debug:
        print("taking off")
        time.sleep(10)
        tello.takeoff()
    # otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # handle the frame from VideoCapture or VideoStream
    frame = tello.get_frame_read().frame if telloStream else vs.read()[1]

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        print("BREAKING")
        break
    
    # track obj
    frame = imutils.resize(frame, width=600) # resize frame to make processing easier
    frame, ocenter, radius = findBlueBall(frame, blueUpper, blueLower, pts, args)

    # move drone
    if( ocenter != None):
        centerObject(frame, ocenter, radius, tello, debug, False)

    # write tello debugging if using tello stream
    if (telloStream):
        textOnFrame(frame, tello)
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        if(not debug):
            print("LANDING")
            tello.land()
        break
# END WHILE

if not debug:
    tello.land()

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
