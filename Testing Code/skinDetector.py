#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:06:07 2016

@author: aman
"""

import numpy as np
import cv2

def getLargestContourArea(contours):
    index = 0
    temp = 0
    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if temp < area:
            temp = area
            index = count
        count = count+1
    return index,temp
    
# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

filename = '/home/aman/Pictures/17.png'
img = cv2.imread(filename)
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
skinMask = cv2.inRange(hsv, lower, upper)

# apply a series of erosions and dilations to the mask
# using an elliptical kernel
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations = 2)
skinMask = cv2.dilate(skinMask, kernel, iterations = 2)

contours, hierarchy = cv2.findContours(skinMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
index = getLargestContourIndex(contours)

zeros = np.zeros(skinMask.shape, dtype=np.uint8)
cv2.drawContours(zeros, contours, index, 255, -1)
ROI = cv2.bitwise_and(gray_img, gray_img, mask=zeros)
cv2.imshow('Extracted skin',ROI)

cv2.imshow('skinMask',skinMask)
cv2.waitKey(0)
cv2.destroyAllWindows()