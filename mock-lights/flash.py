import cv2
import datetime
from flask import Flask, request
from threading import Thread

rows = 6
cols = 18
COLOR_BLACK = (0, 0, 0)
global windows
windows = [[ COLOR_BLACK for x in range(0, cols)] for y in range(0, rows)]

def render():
    while True:
       
        img = cv2.imread('building.png')
        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        x_point = 204
        y_point = 290
        
        for rows in windows: 
            for color in rows:
                cv2.rectangle(img, (x_point, y_point), (x_point + 19, y_point + 23), color, -1)
                x_point = x_point + 29
                y_point = y_point + 1
            y_point = y_point + 43
            x_point = 204
                

        cv2.putText(img=img, text=time_now, org=(20, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),thickness=3)

        cv2.imshow('Building', img)
        
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

new_thread = Thread(target=render)
new_thread.start()


app = Flask(__name__)

@app.route('/light', methods=['GET'])
def light():
    args = request.args
    print(COLOR_BLACK)
    return args

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=5555)

