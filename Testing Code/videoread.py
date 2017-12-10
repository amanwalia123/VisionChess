#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:39:22 2016

@author: aman
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.avi')

while(cap.isOpened()):
ret, frame = cap.read()
frame = cv2.resize(frame,())
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray,(3,3),0)

mat = np.asarray(blur,dtype=np.float32)
[h,w] = (blur.shape[0],blur.shape[1])

ret,thresh = cv2.threshold(blur,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
index = getLargestContourIndex(contours)

zeros = np.zeros(imgray.shape,dtype=np.uint8)
cv2.drawContours(zeros, contours, index, 255, -1)
ROI = cv2.bitwise_and(blur,blur,mask=zeros)



detected_edges = cv2.Canny(ROI,190,200)
dst = cv2.bitwise_and(ROI,ROI,mask = detected_edges)  # just add some colours to edges from original image.


lines = cv2.HoughLines(detected_edges,1,np.pi/180,117)


for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    

    cv2.line(im,(x1,y1),(x2,y2),(0,0,255),2)
cv2.imshow('frame',gray)
if cv2.waitKey(1) & 0xFF == ord('q'):
     break
  
cap.release()
cv2.destroyAllWindows()