#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 03:42:53 2016

@author: aman
"""

import numpy as np
import cv2

filename = '/home/aman/Pictures/Computer_Vision/pulsar.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

(x1,y1)=(301,228)
(x2,y2)=(301,353)
(x3,y3)=(383,353)
(x4,y4)=(301,353)
crop = img[y1:y3,x1:x3]
cv2.imshow("crop",crop)
cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
