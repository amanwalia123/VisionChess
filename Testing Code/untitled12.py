#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:12:00 2016

@author: aman
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
 
filename = "/home/aman/Pictures/Computer_Vision/Project/1.jpg"
img = cv2.imread(file,0)
edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()