#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:54:00 2016

@author: aman
"""

import cv2
import numpy as np

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 0, 0], dtype = "uint8")
upper = np.array([180, 255, 30], dtype = "uint8")

filename = '/home/aman/Pictures/18.png'
img = cv2.imread(filename)
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

black_mask = cv2.inRange(hsv, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

black_mask = cv2.erode(black_mask, kernel, iterations=2)
black_mask = cv2.dilate(black_mask, kernel, iterations=2)

cv2.imshow('Original Image',img)
cv2.imshow('black pieces',black_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

    