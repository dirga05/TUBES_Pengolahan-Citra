import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Pastikan strip setiap baris agar bersih
with open('myDataFile.txt') as f:
    myDataList = [line.strip() for line in f]

while True:
    success, img = cap.read()

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8').strip()

        print("== QR Code Data =", repr(myData))
        print("== In List? ", myData in myDataList)

        if myData in myDataList:
            myOutput = 'Authorized'
            myColor = (0,255,0)
        else:
            myOutput = 'Un-Authorized'
            myColor = (0,0,255)

        if hasattr(barcode, 'polygon'):
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 5)

        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2.left, pts2.top - 10), cv2.FONT_HERSHEY_COMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)
