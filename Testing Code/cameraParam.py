#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 23:05:50 2016

@author: aman
"""

import cv2


#capture from camera at location 0
cap = cv2.VideoCapture(1)
#set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(3,1280)
cap.set(4,1024)
cap.set(15, 0.8)

while True:
    ret, img = cap.read()
    cv2.imshow("input", img)
    #cv2.imshow("thresholded", imgray*thresh2)

    key = cv2.waitKey(10)
    if key == 27:
        break


cv2.destroyAllWindows() 
cv2.VideoCapture(1).release()