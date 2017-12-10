#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:12:31 2016

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
    
im = cv2.imread('/home/aman/Pictures/Computer_Vision/Project/chess1.png')
chessboard = cv2.imread('/home/aman/Pictures/Computer_Vision/Project/chessboard.jpg')
chessboard = cv2.cvtColor(chessboard,cv2.COLOR_BGR2GRAY)
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

# Find the chess board corners
ret1, pts_src = cv2.findChessboardCorners(chessboard, (7,7),None)
#find imaage corners
ret1, pts_dst = cv2.findChessboardCorners(ROI, (7,7),None)

h, status = cv2.findHomography(pts_src, pts_dst)

im_dst = cv2.warpPerspective(ROI, h, (320,320))


cv2.imshow('Warped',chessboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
