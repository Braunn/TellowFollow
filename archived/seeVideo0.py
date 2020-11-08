from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()

#print(tello.get_battery())
tello.streamon()