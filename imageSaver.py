import numpy as np
import cv2

cap = cv2.VideoCapture("/dev/video0")

while(True):
    input('enter something to save another image')
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) # Flip camera vertically

    cv2.imshow('frame', frame)

    cv2.imwrite('ObjImg.jpg',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()