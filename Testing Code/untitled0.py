# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:47:12 2016

@author: aman
"""

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

def mayorContorno(contornos):
	mayor=0;puntosmax=0;i=0; anterior=0
	for cont in contornos:
	#	print puntosmax, len(cont)
		if puntosmax < len(cont):
			anterior=mayor
			mayor = i
			puntosmax=len(cont)
		i = i + 1
	return anterior

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    It = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    It = cv2.adaptiveThreshold(It,127,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7,7)
    contours,hierarchy = cv2.findContours(It, 1, 1)
    mayor = mayorContorno(contours)
    cv2.drawContours(img, contours[mayor], -1, (0,255,0), 2)
    x,y,w,h = cv2.boundingRect(contours[mayor])
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,55,0),3)

    cnt = contours[mayor]
    rect = cv2.minAreaRect(cnt)
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),2)

    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(img,center,radius,(0,255,0),3)
    
    rows,cols = img.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.cv.CV_DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)

    # Display the resulting frame
    #cv2.imshow('Imagen en tiempo t',img)
    cv2.imshow('Imagen contonrnos',It)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()