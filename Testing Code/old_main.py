#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 01:15:26 2016

@author: aman
"""

from framegrabber import *
from modules import *

frames = frame_grabber()

def getLargestContourIndex(contours):
    index = 0
    temp = 0
    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if temp < area:
            temp = area
            index = count
        count = count+1
    return index


def getVerticalLines(image):
    kernelx = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 10))
    dx = cv2.Sobel(image, cv2.CV_16S, 1, 0)
    dx = cv2.convertScaleAbs(dx)
    cv2.normalize(dx, dx, 0, 255, cv2.NORM_MINMAX)
    ret, close = cv2.threshold(dx, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    close = cv2.morphologyEx(close, cv2.MORPH_DILATE, kernelx, iterations=1)
    contour, hier = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x, y, w, h = cv2.boundingRect(cnt)
        if h / w > 5:
            cv2.drawContours(close, [cnt], 0, 255, -1)
        else:
            cv2.drawContours(close, [cnt], 0, 0, -1)
    close = cv2.morphologyEx(close, cv2.MORPH_CLOSE, None, iterations=2)
    return close.copy()



#decide from user to decide whether region of intesrest seleted id correct or not
response = 0
while response == 0:
    #getting frame from framegrabber
    frame = frames.get_frame(1)

    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #blurring the frame with gaussian blur
    blur = cv2.GaussianBlur(imgray,(5,5),0)

    mat = np.asarray(blur, dtype=np.float32)
    [h, w] = (blur.shape[0], blur.shape[1])

    ret, thresh = cv2.threshold(blur, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    index = getLargestContourIndex(contours)

    zeros = np.zeros(imgray.shape, dtype=np.uint8)
    cv2.drawContours(zeros, contours, index, 255, -1)
    ROI = cv2.bitwise_and(blur, blur, mask=zeros)
    cv2.imshow('Extracted Chess board',ROI)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    var = raw_input('Is chess board detected correctly[y\N] ')
    if var == 'y' or var == 'Y':
        response = 1
    else:
        response = 0

while True:

    #getting frame from framegrabber
    frame = frames.get_frame(1)

    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #blurring the frame with gaussian blur
    blur = cv2.GaussianBlur(imgray,(3,3),0)

    mat = np.asarray(blur, dtype=np.float32)
    [h, w] = (blur.shape[0], blur.shape[1])
    ROI = cv2.bitwise_and(blur, blur, mask=zeros)
    detected_edges = cv2.Canny(ROI, 100, 200)
    #vert_edges = getVerticalLines(ROI)
    #detected_edges = cv2.Laplacian(ROI,cv2.CV_64F)
    dst = cv2.bitwise_and(ROI, ROI, mask=detected_edges)  # just add some colours to edges from original image.

    lines = cv2.HoughLines(detected_edges, 1, np.pi / 150, 110)

    if lines is not None:

        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('ROI',ROI)
    cv2.imshow('canny output',detected_edges)
    cv2.imshow('image',frame)
    #cv2.imshow('Vertical Lines',vert_edges)
    time.sleep(0.001)