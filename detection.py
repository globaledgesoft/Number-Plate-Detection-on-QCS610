import cv2
import numpy as np
import sys
sys.path.append('./lib')
import pytesseract
from PIL import Image
import argparse

def capture_image():
    
    cap = cv2.VideoCapture("qtiqmmfsrc ldc=TRUE !video/x-raw, format=NV12, width=1280, height=720, framerate=30/1 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)    
    count = 15
    while(count):             # skipping the initial bluish frame
        count = count - 1 
        ret ,frame = cap.read()
        if(count == 5):
            getNumberPlate(frame)
            break
    cap.release()


def getNumberPlate(image_path):
    image = None
    if(isinstance(image_path,str)):     #image path 
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (620, 480))
    else: #frame
        image = image_path
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 2:
        cnts = cnts[0]
    elif len(cnts) == 3:
        cnts = cnts[1]

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("No contour detected")
        return
    else:
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        cropped = gray[topx:bottomx+1, topy:bottomy+1]
        text = pytesseract.image_to_string(cropped, config='--psm 6')
        print("Detecetd Number Plate :"+ text)
        return text


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--camera", default = "False", required=False, help="Frame is taken from camera ")   
    ap.add_argument("-p", "--image", default = "images/MY70BMW.jpg" , required=False, help=" provide image path")   
    args = vars(ap.parse_args())

    if(args['camera'] == "True"):
        capture_image()
    else: 
        getNumberPlate(args['image'])

