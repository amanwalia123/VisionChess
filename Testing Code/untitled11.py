#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:46:34 2016

@author: aman
"""

import numpy as np
import cv2

im = cv2.imread('/home/aman/Pictures/Computer_Vision/Project/1.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.GaussianBlur(imgray,(9,9),0)
ret,thresh = cv2.threshold(imgray,127,255,0)
imgray = thresh*imgray
detected_edges = cv2.Canny(imgray,125,150)
#dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.


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
    

    cv2.line(im,(x1,y1),(x2,y2),(0,0,255),1)
    
cv2.imshow('detected Edges',im)
cv2.imshow('canny demo',imgray)
#cv2.imshow('segmented image',imgray)
#image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.imshow('thresh',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()