# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:50:29 2016

@author: aman
"""

import numpy as np
from sympy import *
from sympy.geometry import *
import cv2
import random

# Number of iterations for selecting random point pairs
N = 50
# Maximum distance for point to be included
W = 15
# Number of points to take before doing curve fitting
pointCount = 3

# defining a list for storing selected coordinates
coordinates = list()

fileName = "/home/aman/Pictures/Computer_Vision/circles.jpg"


def GetCircle(p1, p2, p3):
    l1 = Line(p1, p2)  # Line passing through points p1 and p2
    l2 = Line(p2, p3)  # Line passing through points p2 and p3

    m1 = l1.slope
    m2 = l2.slope

    P1 = (p1 + p2) / 2
    P2 = (p3 + p2) / 2

    L1 = Line(P1, slope=-1 / m1)
    L2 = Line(P2, slope=-1 / m2)

    c = intersection(L1, L2)[0]
    
    
    radius = c.distance(p1)

    return [c, radius]


def drawCircles():
    while (len(coordinates) > 3):
        temp = 0
        count = 0
        for i in range(N):
            p1, p2, p3 = random.sample(coordinates, 3)
            # print("Selected Points :")
            # print(p1,p2,p3)
            if not ((p1 == p2) and (p2 == p3)):
                #print("Coming here")
                center, radius = GetCircle(p1, p2, p3)
                for point in coordinates:
                    if abs(point.distance(center) - radius) <= W:
                        temp = temp + 1
                if count < temp:
                    (P1, P2, P3) = (p1, p2, p3)
                    count = temp

        [C, R] = GetCircle(P1, P2, P3)
        print("Centre and radius are")
        print(C,float(R))
        # cv2.circle(img,np.int(C),6,(0,0,255),-1)
        # cv2.imshow('image',img)
        arg_points = list()
        for removal_point in coordinates:
            if (abs(C.distance(removal_point) - R) <= W):
                arg_points.append(removal_point)
                coordinates.remove(removal_point)
        # print(args_points)
        #args = np.int(arg_points)
        #print("Points differentiated are")
        #print(arg_points)
        # if(len(args)>1):


def mark(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 76, (0, 0, 255), -1)
        cv2.imshow('image', img)
        coordinates.append(Point2D(x, y))
        if (len(coordinates) == pointCount+1):
            drawCircles()

# Read from image from filesystem
img = cv2.imread(fileName, cv2.IMREAD_COLOR)

w = img.shape[1]

# Naming windows for image display
cv2.namedWindow('image')

# set mouse call event for recording clicks
cv2.setMouseCallback('image', mark)

cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()    





