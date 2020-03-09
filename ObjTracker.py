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





def HeadMove(Coord):
    if Coord[0]>(width//2)+20:
        ArdSer.SendStringCommand("b")
    elif Coord[0]<(width//2)+40:
        ArdSer.SendStringCommand("a")
    print(ArdSer.SerialReadLines())



# HSV фильтр данные которого мы записали использую предыдущую программу.
hsv_min = np.array((0, 38, 30), np.uint8)
hsv_max = np.array((23, 127, 166), np.uint8)

while True:
    flag, img = cap.read()
    M = cv2.getRotationMatrix2D(center, 270, 1)
    img = cv2.warpAffine(img, M, (int(width), int(height)))
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
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
        HeadMove((x,y))

    cv2.imshow('result', img)


    ch = cv2.waitKey(35)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()