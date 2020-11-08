import cv2
import numpy as np

im = cv2.cv2.imread("pictures/back.jpg")

lower_b = np.array([300,100,100])
upper_b = np.array([300,100,0])

frameHSV = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(frameHSV, lower_b, upper_b)
res = cv2.bitwise_and(im, im, mask=mask)    # Show the first mask
cv2.imshow('mask', mask)
cv2.imshow('res', res)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
x,y,w,h = cv2.boundingRect(biggest_contour)
cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)

cv2.putText(im, "PUT ANYTHING HERE", (5, 240-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
cv2.imshow('Image', im)

if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()