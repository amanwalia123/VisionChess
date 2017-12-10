# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:16:28 2016

@author: aman
"""

import cv2

filePath = "/home/aman/Pictures/triangle.jpg"

img = cv2.imread(filePath)

while(1):
    cv2.imshow('image',img)

    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()