import numpy as np
import cv2


cap = cv2.VideoCapture('udpsrc port=5000 caps="application/x-rtp,\
                        payload=96" ! rtph264depay ! queue ! avdec_h264 ! videoconvert ! appsink'
                       ,cv2.CAP_GSTREAMER)

while True:
    ret,frame = cap.read()
    if not ret:
        print('empty frame')
        continue
    cv2.imshow('receive', frame)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
cap.release()
cap.receive()