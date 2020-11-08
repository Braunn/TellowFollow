from djitellopy import Tello
import cv2
import time

tello = Tello()

tello.connect()

tello.takeoff()

#tello.move_left(1)
tello.move_up(20)
time.sleep(10)
tello.move_forward(20)
time.sleep(10)
tello.move_back(20)
time.sleep(10)
tello.rotate_counter_clockwise(90)
time.sleep(10)
tello.move_forward(10)
time.sleep(10)
tello.move_back(10)
time.sleep(10)

tello.land()
