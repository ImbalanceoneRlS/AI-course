from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import ArdSerial.ArdSender as As

cv2.namedWindow( "result" )

cap = cv2.VideoCapture("/dev/video0")
width  = cap.get(3) # float
height = cap.get(4) # float
center = (width//2,height//2)
ArdSer = As.ArdunoSender()
ArdSer.SendStringCommand("i")
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_default.xml')




def HeadMove(Coord):
    if Coord[0]>(width//2)+20:
        ArdSer.SendStringCommand("b")
    elif Coord[0]<(width//2)-20:
        ArdSer.SendStringCommand("a")
    print(ArdSer.SerialReadLines())

def FaceDetection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor= 1.1,
        minNeighbors= 5,
        minSize=(10, 10)
    )
    # Рисуем квадраты вокруг лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    if len(faces)>0:
        return image,faces[0][0]+faces[0][2]//2,faces[0][1]+faces[0][3]//2
    else:
        return image,None,None


# HSV фильтр данные которого мы записали использую предыдущую программу.
hsv_min = np.array((109,180,110), np.uint8)
hsv_max = np.array((123,237,167), np.uint8)
flag, img = cap.read()
flag, img = cap.read()
while True:
    flag, img = cap.read()
    M = cv2.getRotationMatrix2D(center, 270, 1)
    img = cv2.warpAffine(img, M, (int(width), int(height)))
    img,x,y = FaceDetection(img)
    if x != None and y!= None:
        HeadMove((x,y))
    cv2.imshow('result', img)


    ch = cv2.waitKey(35)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()