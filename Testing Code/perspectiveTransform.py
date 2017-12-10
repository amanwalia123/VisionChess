#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:10:21 2016

@author: aman
"""

# import the necessary packages
import numpy as np
import cv2
 
coordinates = []

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
	# return the warped image
	return warped
 
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),4,(0,255,0),-1)
        coordinates.append((x,y))
    
            
        
        
filename = '/home/aman/Pictures/18.png'
img = cv2.imread(filename)
clone = img.copy()
cv2.namedWindow('Chessboard')
cv2.setMouseCallback('Chessboard',draw_circle)

while True:
    cv2.imshow('Chessboard',img)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('r'):
        img = clone.copy()
    if key == ord('c'):
        break
if len(coordinates) == 4:
    chess = four_point_transform(img,np.asarray(coordinates))
cv2.destroyAllWindows() 

cv2.imshow('ROI',chess)

gray_chess = cv2.cvtColor(chess,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray_chess,(1,1),0)
detected_edges = cv2.Canny(blur,50,200)
dst = cv2.bitwise_and(gray_chess,gray_chess,mask = detected_edges)  
dilated = cv2.dilate(detected_edges, np.ones((7, 7)))
cv2.imshow('Edges',dilated)

cv2.waitKey(0)
cv2.destroyAllWindows()    
    
    



