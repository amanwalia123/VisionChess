from modules import *


class SkinDetector(object):

    def __init__(self,lower,upper,skinThresh):

        # HSV Model for skin color using upper and lower threshold values
        self.lskinRange = lower
        self.uskinRange = upper

        # parameter to decide how much skin area is sufficient to reject the frame
        self.skinAreaThresh = skinThresh

        # five states of skin detector which are initially set to true to initially detect that skin is there,
        # this is just transition step and hence will not create problem
        self.skin_state1 = True
        self.skin_state2 = True
        self.skin_state3 = True
        self.skin_state4 = True
        self.skin_state5 = True

    def get_largest_contour_area(self,contours):
        index = 0
        temp = 0
        count = 0
        for c in contours:
            area = cv2.contourArea(c)
            if temp < area:
                temp = area
                index = count
            count += 1
        return index, temp

    def get_frame_area(self,frame):
        (width,height,dim) = frame.shape
        return width*height

    def check_skin(self,frame):

        frame_area = self.get_frame_area(frame)
        skin_area = self.get_skin_area(frame)

        rel_skin_area = skin_area/frame_area
        if rel_skin_area < self.skinAreaThresh:
            return self.skin_state_stabiliser(False)
        else:
            return self.skin_state_stabiliser(True)


    def get_skin_area(self,frame):
        # converting the frame to HSV color space to apply skin detection model
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #grayscale frame
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # detecting all the pixels which are lying in range of skin color model
        skin_mask = cv2.inRange(hsv_frame, self.lskinRange, self.uskinRange)

        # apply a series of erosions and dilations to the mask
        # using an elliptical kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skin_mask = cv2.erode(skin_mask, kernel, iterations=2)
        skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)

        # detecting the contours on skin blobs
        contours, hierarchy = cv2.findContours(skin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #getting index of the largest contour and its area
        index,skin_area = self.get_largest_contour_area(contours)

        zeros = np.zeros(gray_frame.shape, dtype=np.uint8)
        cv2.drawContours(zeros, contours, index, 255, -1)
        ROI = cv2.bitwise_and(gray_frame, gray_frame, mask=zeros)
        cv2.imshow('Detected Skin',ROI)

        return skin_area

    # This function is necessary to remove bumpy reading from skin detector as during transition phase detector
    # reading oscillate between False and True, Hence for stabilising this five consecutive false are required to make
    # detector vote for no skin detected, hence transition phase is tackled.
    def skin_state_stabiliser(self,skin_curr_state):
        res = self.skin_state1 or self.skin_state2 or self.skin_state3 or self.skin_state4 or self.skin_state5
        self.skin_state5 = self.skin_state4
        self.skin_state4 = self.skin_state3
        self.skin_state3 = self.skin_state2
        self.skin_state2 = self.skin_state1
        self.skin_state1 = skin_curr_state
        return res
