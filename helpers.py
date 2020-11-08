import cv2
import numpy as np
import imutils

def in2cm(inches):
    return inches*2.54

def textOnFrame(frame, tello):
    texts = getStatusTexts(tello)

    h, w, c = frame.shape
    h_offset = h - 5
    for text in texts:
        cv2.putText(frame, text, (5, h_offset),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        h_offset = h_offset - 15

def getStatusTexts(tello):
    mp_str = "Mission Pad: {}".format(tello.get_mission_pad_id())
    bat_str = "Battery: {}%".format(tello.get_battery())
    temp_str = "Temperature: {} F".format(round(tello.get_temperature() * (9 / 5) + 32), 1)
    alt_str = "Altitude: {}cm".format(tello.get_distance_tof())

    texts = [mp_str, bat_str, temp_str, alt_str]

    return texts

def findBlueBall(frame, upper, lower, pts, args):
    # resize the frame, blur it, and convert it to the HSV
    # color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "blue", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower, upper)  # mask out everything that is blue
    mask = cv2.erode(mask, None, iterations=2)  # erode small spots of blue
    mask = cv2.dilate(mask, None, iterations=2)  # now that small spots are gone, make remains bigger!

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    radius = None

    # only proceed if at least 1 contour, ball is in frame
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
                       (0, 255, 255), 2)  # surround ball
            cv2.circle(frame, center, 5, (0, 0, 255), -1)  # surround center

        # update queue
        pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)  # thickness dependent on time not radius /!\
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    return [frame, center, radius]

def centerObject(frame, ocenter, radius, tello, debug, lock):
    # print("IN CENTER OBJECT")
    # consider adding delay to let drone move
    FOV = 86.2 # tello FOV in degrees

    x,y = ocenter

    # consider replacing with just the values?
    height, width = frame.shape[:2] # gets dimensions of frame, x is horizontal left to right 0-600, y is vertical top to bot 0-450
    xc = int(width/2)
    yc = int(height/2)

    rc = 67 # experimentally determined value for centered radius max is ~200 min ~10
    depth = 200-10

    # parameters that determine movement size, and when to move
    yMinStep = 20 # see documentation
    rotateStep = 25 #(FOV*10/3600) * width/25 # 3600 is the max rotation, FOV*10 is the equivalent coverage of drone camera
    ystep = 5 # height/20 # up and down translational step
    zstep = 20 # depth/20 # foward and backward step

    xgain = (x-xc)/xc
    ygain = (y-yc)/yc
    rgain = (radius-rc)/rc

    ythreshold = 0.2
    rotateThreshold = 0.2
    rthreshold = 0.25

    #print(ocenter, " true center: ", trueCenter, " radius: ", radius)

    # make the drone move so ball is centered
    if not debug:
        # turning is is priority to keep ball in track, next is up and down, last is fw and bw?
        #xyzOpen = [True, True, True] # to prevent one movement from monopolizing each run, it is locked, NEEDS TO BE MOVED

        #if not(lock) and xyzOpen[0]:
        #left and right rotating
        rmove = int(abs(xgain)*rotateStep)
        if xgain < -rotateThreshold:
            tello.rotate_counter_clockwise(rmove)
        elif xgain > rotateThreshold:
            tello.rotate_clockwise(rmove)

        # close moving rotating and open other movement
        #xyzOpen[0] = False
        #xyzOpen[1:] = [True, True]

        #if not(lock) and xyzOpen[1]:
        # up and down
        ymove = int(abs(ygain)*ystep+yMinStep)
        if ygain < -ythreshold:
            tello.move_up(ymove)
        elif ygain > ythreshold:
            tello.move_down(ymove)

        # close y movement open others
        #xyzOpen[1] = False
        #xyzOpen[0] = True
        #xyzOpen[2] = True

        #if not(lock) and xyzOpen[2]
        # forward and backward movement, worked well with current gain: might be able to go a bit larger in step
        zmove = int(abs(rgain)*zstep+yMinStep)
        if rgain < -rthreshold:
            print("FOWARD: ", zmove)
            tello.move_forward(zmove)
        elif rgain > rthreshold:
            print("BACKWARD: ", zmove)
            tello.move_back(zmove)

    else:
        # print("IN DEBUG")
        color = (255,0,0)
        thickness = 9
        endpoint = (xc,yc)

        if ygain < -ythreshold:
            # up
            cv2.arrowedLine(frame, (xc, height), endpoint , color, thickness)
        elif ygain > ythreshold:
            # down
            cv2.arrowedLine(frame, (xc, 0), endpoint, color, thickness)

        # left and right rotating
        if xgain < -rotateThreshold:
            # left
            cv2.arrowedLine(frame, (width, yc), endpoint, color, thickness)
        elif xgain > rotateThreshold:
            # right
            cv2.arrowedLine(frame, (0,yc), endpoint, color, thickness)

        # forward and backward movement
        if rgain < -rthreshold:
            # forwards
            cv2.putText(frame, "go forward", (5, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif rgain > rthreshold:
            # backwards
            cv2.putText(frame, "go backward", (5, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)