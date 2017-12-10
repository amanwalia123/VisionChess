#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 02:05:51 2016

@author: aman
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, orig_img = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    w = gray.shape[0]
    h = gray.shape[1]

    

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    
    mat = np.float32(gray)
    avg = np.int(sum(sum(mat))/(w*h))
    th, im_th = cv2.threshold(gray, avg, 255, cv2.THRESH_BINARY);
     
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
     
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
     
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
     
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
     
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv
    
    checker_board = im_out*gray 
# Display images.
    cv2.imshow("Thresholded Image", im_th)
    cv2.imshow("Floodfilled Image", im_floodfill)
    cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
    cv2.imshow("Foreground", im_out)
    cv2.imshow("CheckerBoard",checker_board)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()