import cv2
import numpy as np
import time

'''
Parameters Used inside Code
'''
#Gaussian kernel size used for blurring
G_kernel_size = (3,3)

#canny thresholding parameters
canny_u_threshold = 200
canny_l_threshold = 80


# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")


black_lower = np.array([0, 0, 0], dtype = "uint8")
black_upper = np.array([180, 255, 30], dtype = "uint8")

#threshhold for % of skin area detected
skinThresh = 0.00025

#Minimum number of whitepixels needed for square to be counted as occupied
min_white_count = 1
#minimum number of black detected pixels in square
min_black_pixels = 200