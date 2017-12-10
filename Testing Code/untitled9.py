#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 00:58:45 2016

@author: aman
"""

import numpy as np
import cv2
from sympy import Point2D

def getLargestContourIndex(contours):
    index = 0
    temp = 0
    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if temp < area:
            temp = area
            index = count
        count = count+1
    return index

def mergeSimilarLines(lines,width,height):
    if lines is None:
        return None
    else:
        lines_list = lines.toList() 
        
        for l1 in lines_list:
            for l2 in lines_list:
                if not((l1 == l2)):
                    p1 = l1[1]
                    p2 = l2[1]
                    theta1 = l1[0]
                    theta2 = l2[0]

                    if theta1 > np.pi*45/180 and theta1 < np.pi*135/180:
                        P1 = Point2D(0,p1/np.sin(theta1))
                        P2 = Point2D(width,-width/np.tan(theta1)+p1/np.sin(theta1))
                    else:
                        P1 = Point2D(0,p1/np.cos(theta1))
                        P2 = Point2D(-height/np.tan(theta1)+p1/np.cos(theta1),height)

                    
#filename = '/home/aman/Pictures/Computer_Vision/Project/chess1.png'
filename = '/home/aman/Pictures/chess1.png'                    
           
im = cv2.imread(filename)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray,(3,3),0)

mat = np.asarray(blur,dtype=np.float32)
[h,w] = (blur.shape[0],blur.shape[1])

ret,thresh = cv2.threshold(blur,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
index = getLargestContourIndex(contours)

zeros = np.zeros(imgray.shape,dtype=np.uint8)
cv2.drawContours(zeros, contours, index, 255, -1)
ROI = cv2.bitwise_and(imgray,imgray,mask=zeros)

kernel = np.ones((5,5),np.uint8)
ROI_er = cv2.erode(ROI,kernel,iterations = 1)

detected_edges = cv2.Canny(ROI,100,200)
dst = cv2.bitwise_and(ROI,ROI,mask = detected_edges)  # just add some colours to edges from original image.


lines = cv2.HoughLines(detected_edges,1,np.pi/150,110)



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
    
corners = cv2.goodFeaturesToTrack(ROI,130,0.01,10)
corners = np.int0(corners)
for i in corners:
    x,y = i.ravel()
    cv2.circle(im,(x,y),3,(255,0,0),2)      
    
    
cv2.imshow('detected Edges',im)
#roi = cv2.mean(imgray,mask=mask)
cv2.imshow('Blurred Image',blur)
cv2.imshow('ROI',ROI)
cv2.waitKey(0)
cv2.destroyAllWindows()


        