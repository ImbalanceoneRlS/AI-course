import cv2
import numpy as np
import sys
import os



cap = cv2.VideoCapture("/dev/video0")

#out_send = cv2.VideoWriter('appsrc ! queue ! videoconvert ! video/x-raw ! omxh264enc ! video/x-h264 ! h264parse ! rtph264pay ! udpsink host=192.168.1.17 port=5000 sync=false',0,25.0,(640,480))

print('test1')

while True:
    ret,frame = cap.read()

    if not ret:
        print('empty frame')
        break

    #out_send.write(frame)
    os.write( 1, frame.tostring())
    #cv2.imshow('send', frame)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break