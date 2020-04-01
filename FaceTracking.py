from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import ArdSerial.ArdSender as As
#import sounds.ttsGoogleTranslateAPI as ttsGT
#import sounds.Govorilka as Govor
import subprocess as sp

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=camera.resolution)
time.sleep(0.1)
cap = cv2.VideoCapture("/dev/video0")
width  = camera.resolution[0]#cap.get(3) # float
height = camera.resolution[1]#cap.get(4) # float
center = (width//2,height//2)
ArdSer = As.ArduinoSender()
ArdSer.SendStringCommand("i")
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_default.xml')


# e - закрыть рот f открыть рот  G H I обнуления

def HeadMove(Coord):
    if Coord[0]>(width//2)+10:
        ArdSer.SendStringCommand("d")
    elif Coord[0]<(width//2)-10:
        ArdSer.SendStringCommand("c")
    if Coord[1]>(height//2)+10:
        ArdSer.SendStringCommand("b")
    elif Coord[1]<(height//2)-10:
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
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    if len(faces)>0:
        return image,faces[0][0]+faces[0][2]//2,faces[0][1]+faces[0][3]//2
    else:
        return image,None,None


cv2.namedWindow( "result" )
FlTime = 0
FlagFace = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    img,x,y = FaceDetection(img)
    if x != None and y!= None:
        if FlagFace == 0:
            FlagFace = 1
            print(time.time()-FlTime)

            if time.time()-FlTime > 7:
                FlTime = time.time()
                sp.Popen("python3 /home/pi/AIcurs/sounds/Govorilka.py "+"приветствую вас",shell = True)
        FlTime = time.time()
        HeadMove((x,y))
    else:
        FlagFace = 0
    cv2.imshow('result', img)


    ch = cv2.waitKey(35)
    if ch == 27:
        break
    rawCapture.truncate()
    rawCapture.seek(0)

cap.release()
cv2.destroyAllWindows()