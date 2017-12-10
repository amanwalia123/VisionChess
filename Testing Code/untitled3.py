# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 20:34:45 2016

@author: aman
"""
import cv2
import numpy as np


filename = '/home/aman/Pictures/Computer_Vision/Project/1.jpg'


orig_img = cv2.imread(filename,0)

w = orig_img.shape[0]/2
h = orig_img.shape[1]/2

img = cv2.resize(orig_img,(w,h))

img_blur =cv2.GaussianBlur(img,(5,5),0)
mat = np.int32(img_blur)
avg_val = sum(sum(mat))/(w*h)
thresh_image = np.zeros((img.shape),dtype=np.float32) 

for i in range(0,h,1):
    for j in range(0,w,1):
        if img_blur[i,j] > avg_val:
            thresh_image[i,j] = 1.00

h, w = thresh_image.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
im_floodfill = thresh_image.copy()
# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0,0), 255);
 
# Invert floodfilled image
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
 
# Combine the two images to get the foreground.
im_out = thresh_image | im_floodfill_inv
cv2.imshow('Thresholded Image',thresh_image)
cv2.imshow('Gaussian Blur',img_blur)
cv2.imshow('Board',board)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.Canny


