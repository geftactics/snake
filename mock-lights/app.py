import cv2
import datetime
import glob
import os

COLOR_BLACK = (0, 0, 0)
rows = 6
cols = 18
windows = [[ COLOR_BLACK for x in range(0, cols)] for y in range(0, rows)]


while True:
       
    img = cv2.imread('building.png')
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(img=img, text=time_now, org=(20, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),thickness=3)

    x_point = 204
    y_point = 290

    for filename in glob.glob('*.dat'):
        print(filename)
        with open(filename, 'r') as file:
            data = file.read().rstrip().split(',')
            x = int(data[1])
            y = int(data[0])
            color = int(data[4]), int(data[3]), int(data[2])
            windows[x][y] = color
            print(data)
        os.remove(filename)
    
    for rows in windows: 
        for color in rows:
            cv2.rectangle(img, (x_point, y_point), (x_point + 19, y_point + 23), color, -1)
            x_point = x_point + 29
            y_point = y_point + 1
        y_point = y_point + 43
        x_point = 204
            
    cv2.imshow('Building', img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

    