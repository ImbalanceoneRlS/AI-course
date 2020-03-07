import cv2
import numpy as np


cv2.namedWindow( "result" )

cap = cv2.VideoCapture("/dev/video0")
# HSV фильтр данные которого мы записали использую предыдущую программу.
hsv_min = np.array((116, 143, 42), np.uint8)
hsv_max = np.array((138, 235, 97), np.uint8)

color_yellow = (0,255,255)

while True:
    flag, img = cap.read()
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV )
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
        cv2.circle(img, (x, y), 10, color_yellow, -1)
        cv2.putText(img, "%d-%d" % (x,y), (x+10,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)


    cv2.imshow('result', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()