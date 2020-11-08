from djitellopy import Tello
import cv2
import numpy as np
tello = Tello()
tello.connect()
tello.streamon()
def nothing(*arg):
    pass
def get_resized_frame(w=360,h=240):
    return cv2.resize(tello.get_frame_read().frame,(w,h))

lower_purp = np.array([300,100,100])
upper_purp = np.array([300,100,0])

def nothing(*arg):
    pass

icol = (0, 0, 0, 255, 255, 255)   # New start

cv2.namedWindow('colorTest')
# Lower range colour sliders.
cv2.createTrackbar('lowHue', 'colorTest', icol[0], 255, nothing)
cv2.createTrackbar('lowSat', 'colorTest', icol[1], 255, nothing)
cv2.createTrackbar('lowVal', 'colorTest', icol[2], 255, nothing)
# Higher range colour sliders.
cv2.createTrackbar('highHue', 'colorTest', icol[3], 255, nothing)
cv2.createTrackbar('highSat', 'colorTest', icol[4], 255, nothing)
cv2.createTrackbar('highVal', 'colorTest', icol[5], 255, nothing)

while True:
    bat = tello.get_battery()
    temp = tello.get_temperature()

    lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
    lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
    lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')

    highHue = cv2.getTrackbarPos('highHue', 'colorTest')
    highSat = cv2.getTrackbarPos('highSat', 'colorTest')
    highVal = cv2.getTrackbarPos('highVal', 'colorTest')

    frame = get_resized_frame()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    colorLow = np.array([lowHue,lowSat,lowVal])
    colorHigh = np.array([highHue,highSat,highVal])
    mask = cv2.inRange(frameHSV, colorLow, colorHigh)
    res = cv2.bitwise_and(frame, frame, mask=mask)    # Show the first mask
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    x,y,w,h = cv2.boundingRect(biggest_contour)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    text = "Battery: {}%".format(tello.get_battery())
    cv2.putText(frame, text, (5, 240-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()