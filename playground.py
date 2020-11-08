import cv2
import numpy as np
import imutils

vs = cv2.VideoCapture("./pictures/ballVideo.mp4")

while True:
    frame = vs.read()[1]
    frame = imutils.resize(frame, width=600)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    elif key == ord("w"):
      input(frame.shape)


"""
im = cv2.imread("pictures/back.jpg")
imHSV = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
labIm = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)

calim = cv2.imread("pictures/ballZoom.png")
calim = cv2.cvtColor(calim,cv2.COLOR_BGR2HSV)
hsvMax = [np.max(calim[:,:,0]),np.max(calim[:,:,1]),np.max(calim[:,:,2])]
hsvMin = [np.min(calim[:,:,0]),np.min(calim[:,:,1]),np.min(calim[:,:,2])]

print(hsvMax,hsvMin)

#cv2.imshow("pic",im[:,:,2])
#cv2.waitKey(0)
"""
"""
# upper, right
limit = im.shape

def nothing(*arg):
    pass

cv2.namedWindow('colorTest')
cv2.createTrackbar('top', 'colorTest', 0, limit[0], nothing)
cv2.createTrackbar('bot', 'colorTest', 0,limit[0], nothing)
cv2.createTrackbar('rightb', 'colorTest', 0, limit[1], nothing)
cv2.createTrackbar('leftb', 'colorTest', 0, limit[1], nothing)

bot, right = limit[:2]
top, left = [0, 0]

while True:

    cv2.imshow("crop", im[top:bot, left:right, :])
    cv2.waitKey(0)

    top = cv2.getTrackbarPos('top', 'colorTest')
    bot = cv2.getTrackbarPos('bot', 'colorTest')
    right = cv2.getTrackbarPos('rightb', 'colorTest')
    left = cv2.getTrackbarPos('leftb', 'colorTest')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

#plotColorSpace(im[top:bot, left:right, :])
"""