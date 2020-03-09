import cv2
import numpy as np

def createPath( img ):
    h, w = img.shape[:2] #так как массив изображения трехмерный, мы возьмем только 2 первых параметра высоты и ширину
    return np.zeros((h, w, 3), np.uint8)

cv2.namedWindow( "result" )

cap = cv2.VideoCapture("/dev/video0")
# HSV фильтр данные которого мы записали использую предыдущую программу.
hsv_min = np.array((116, 143, 42), np.uint8)
hsv_max = np.array((138, 235, 97), np.uint8)

lastx = 0 #переменные в которых будем хранить предыдущие координаты найденного объекта
lasty = 0
path_color = (0,0,255) #добавляем кортеж с указанием цвета в !!!формате BGR!!!
flag, img = cap.read()
# создаем пустое изображение такого же размера как первый захваченный кадр
path = createPath(img) # на котором мы будем рисовать наш путь и в котором будем его сохранять.


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
        cv2.circle(img, (x, y), 10, (0,0,255), -1)
    else: # если объект не найден ставим переменные координат равными нулю и ничего не рисуем
        x=0
        y=0
        lastx=0
        lasty=0

    if lastx > 0 and lasty > 0:# если не первый кадр с нулями, то
        cv2.line(path, (lastx, lasty), (x,y), path_color, 5)
    lastx = x
    lasty = y

    # накладываем линию траектории поверх изображения
    img = cv2.add( img, path)

    cv2.imshow('result', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()