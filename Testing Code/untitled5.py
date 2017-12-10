import cv2
import numpy as np
from scipy.interpolate import interpolate
import random
from sympy import Point , Line

#Number of iterations for selecting random point pairs
N = 500
#Maximum distance for point to be included
D = 5
# Number of points falling within this distance
count = 0

#Two points
P1 = Point(0,0)
P2 = Point(0,0)

#defining set for storing coordinates recorded by mouse clicks
coordinates = list()

# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(new_img,(x,y),3,(0,0,255),-1)
        coordinates.append((x,y))


def draw_besfit():

    while(len(coordinates)>0):

        temp = 0
        count = 0

        #print(coordinates)
        #converting set of coordinates to vector
        points = np.asanyarray(coordinates)

        for i in range(N):
            (x1,y1),(x2,y2) = random.sample(coordinates,2)      #selecting two random points
            p1 = Point(x1,y1)
            p2 = Point(x2, y2)
            line = Line(p1,p2)                                  #Line through p1 and p2
            for point in points:
                (x,y) = point
                p = Point(x,y)
                if line.distance(p) <= D:
                    temp = temp + 1
            if count < temp:
                count = temp
                P1 = p1
                P2 = p2
            temp = 0

        p_line = Line(P1,P2)        # line passing through points having maximum number of points in distance less than D

        p_list = list()             #list of points which are at distance less than D from line(P1,P2)
        for point in points:
            (x,y) = point
            p = Point(x,y)
            if p_line.distance(p) <= D:
                p_list.append(p)
                coordinates.remove((x,y))
        print(p_list)
        args = np.float32(p_list)
        (vx, vy, cx, cy) = cv2.fitLine(args, 2, 0, 0.01, 0.01)
        cv2.line(new_img, (int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w)), (0, 255, 0),4)





# Read from image from filesystem
img = cv2.imread("/home/aman/PycharmProjects/Linefit/dark_rect.jpg",cv2.IMREAD_COLOR)

#resizing the image
newx,newy = img.shape[1]/2,img.shape[0]/2
new_img = cv2.resize(img,(newx,newy))
w =  img.shape[1]

#Naming windows for image display
cv2.namedWindow('image')

#set mouse call event for recording clicks
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',new_img)
    if (len(coordinates) >= 20):
        draw_besfit()

    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()