#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 05:02:39 2016

@author: aman
"""

import cv2
import numpy as np

filename = '/home/aman/Pictures/Computer_Vision/Project/1.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray_blur = cv2.GaussianBlur(gray,(7,7),0)

detected_edges = cv2.Canny(gray_blur,100,200)

 
dst = cv2.cornerHarris(detected_edges,2,1,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.3*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()