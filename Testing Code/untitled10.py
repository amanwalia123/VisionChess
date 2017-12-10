#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 22:13:56 2016

@author: aman
"""
import cv2
import numpy as np
img = cv2.imread('/home/aman/Pictures/Computer_Vision/Project/1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



blur = cv2.GaussianBlur(gray,(9,9),0)

detected_edges = cv2.Canny(detected_edges,125,150)
dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.


lines = cv2.HoughLines(detected_edges,1,np.pi/180,115)


for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
    
cv2.imshow('detected Edges',detected_edges)
cv2.imshow('canny demo',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
