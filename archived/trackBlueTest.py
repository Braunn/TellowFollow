import cv2
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

backIm = cv2.imread("pictures/back.jpg")
labIm = cv2.cvtColor(backIm, cv2.COLOR_BGR2LAB)

plotColorSpace(backIm[481:708,1108:1323,:])


"""
#range for mask
blue_max = (255,0,0)
blue_min = (200,0,0)

sideLen = int(0.5e3)
lo_square = np.full((sideLen, sideLen, 3), blue_max, dtype=np.uint8) / 255.0
hi_square = np.full((sideLen, sideLen, 3), blue_min, dtype=np.uint8) / 255.0

cv2.imshow("lo",lo_square)
cv2.imshow("hi",hi_square)
cv2.waitKey(0)
cv2.destroyAllWindows()

mask = cv2.inRange(backIm, blue_max, blue_min)
filtered = cv2.bitwise_and(backIm,backIm,mask=mask)

print(type(mask))

cv2.imshow("filtered", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# only take  channels
labIm[:,:,0] = 0
labIm[:,:,2] = 0

plt.imshow(backIm[:,:,0], cmap='gray', vmin=0, vmax=255)
plt.show()

cv2.imshow('pic',labIm)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""