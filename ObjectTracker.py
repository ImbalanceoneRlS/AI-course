from picamera.array import PiRGBArray
from picamera import PiCamera
import time,cv2,numpy as np
import ArdSerial.ArdSender as As


camera = PiCamera() #подключаемся к камере через библиотек Rpi
camera.resolution = (640, 480)
camera.framerate = 30
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=camera.resolution)
time.sleep(0.1)
width  = camera.resolution[0]#cap.get(3) # float
height = camera.resolution[1]#cap.get(4) # float
center = (width//2,height//2)#находим центр изображения
ArdSer = As.ArduinoSender() # подключаемся к Arduino
ArdSer.SendStringCommand("i") # просим уйти в значение по умолчанию



def HeadMove(Coord):
    if Coord[0]>(width//2)+10:
        ArdSer.SendStringCommand("d")
    elif Coord[0]<(width//2)-10:
        ArdSer.SendStringCommand("c")
    if Coord[1]>(height//2)+10:
        ArdSer.SendStringCommand("b")
    elif Coord[1]<(height//2)-10:
        ArdSer.SendStringCommand("a")
    print(ArdSer.SerialReadLines())# обязательно считываем данные которые пришли что бы очистить буфер


cv2.namedWindow("result")
hsv_min = np.array((109,180,110), np.uint8)
hsv_max = np.array((123,237,167), np.uint8)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)


    # вычисляем моменты изображения
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
    # будем реагировать только на те моменты,
    # которые содержать больше 100 пикселей
    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 10, (0,0,255), -1)
        #вызываем функцию движения головы передавая в нее координаты объекта
        HeadMove((x,y))
    else:
        FlagFace = 0
    cv2.imshow('result', img)


    ch = cv2.waitKey(35)
    if ch == 27:
        break
    rawCapture.truncate()
    rawCapture.seek(0)

cv2.destroyAllWindows()