from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()t =

#print(tello.get_battery())
tello.streamon()
def get_resized_frame(w=360,h=240):
    return cv2.resize(tello.get_frame_read().frame,(w,h))

while True:
    cv2.imshow('Image', get_resized_frame())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break