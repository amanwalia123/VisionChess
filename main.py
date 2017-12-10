from PerspectiveTransform import PerspectiveTransform
from framegrabber import *
from modules import *
from ChessSquare import *
from SkinDetector import *
from chessBoard import *


def sharpen_image(frame):
    # Create the identity filter, but with the 1 shifted to the right!
    kernel = np.zeros((9, 9), np.float32)
    kernel[4, 4] = 2.0  # Identity, times two!
    # Create a box filter:
    boxFilter = np.ones((9, 9), np.float32) / 81.0
    # Subtract the two:
    kernel = kernel - boxFilter
    # Note that we are subject to overflow and underflow here...but I believe that
    # filter2D clips top and bottom ranges on the output, plus you'd need a
    # very bright or very dark pixel surrounded by the opposite type.
    return cv2.filter2D(frame, -1, kernel)


#frame grabber object to grab frames
frames = frame_grabber()

# Create a new instance of the board interface for a new game
boardInterface = BoardInterface()

#object of class skin Detector
skinDetector = SkinDetector(lower,upper,skinThresh)

#Determining homorgraphy matrix for chess board
init_frame = frames.get_frame()
perspectransform = PerspectiveTransform(init_frame)
init_per_frame = cv2.warpPerspective(init_frame, perspectransform.transfmatrix, perspectransform.dim)

#Chess square corners
(width,height) = perspectransform.dim
x = np.linspace(0,width,9,dtype=np.int)
y = np.linspace(0,height,9,dtype=np.int)

#predicted corners of chess board based on dimension calculation
pred_corners = np.transpose([np.tile(x,len(y)),np.repeat(y,len(x))])
pred_corners_list = pred_corners.tolist()

#reshaping the corners to make it suitable for conevrsion into chess square format
pred_corners = pred_corners.reshape(9, 9, 2)
pred_corners_list1 = pred_corners.tolist()

#using these corners to initialise multidimensional array of chess squares class
corners = np.zeros((8,8,4,2),dtype=np.int)
for i in range(0,8):
    for j in range(0,8):
        corners[i,j,0] = pred_corners[i,j]
        corners[i,j,1] = pred_corners[i+1,j]
        corners[i,j,2] = pred_corners[i+1,j+1]
        corners[i,j,3] = pred_corners[i,j+1]

#list of chess square objects
squares = []
# Declaring chess square object relating to its (x,y) & associating corners to it and initial cropped image of that square
for x in range(0,8):
    for y in range(0,8):
        s = ChessSquare((x,y),corners[x,y],init_per_frame,min_white_count,min_black_pixels)
        squares.append(s)

# setting font for text
font = cv2.FONT_HERSHEY_SIMPLEX

(w, h) = perspectransform.dim


'''
This is main loop where all the processing happens, a frame is grabbed from frame-grabber class
and perspective projection is applied to it to extract the ROI i.e. chessboard. After that
'''
while True:
    # frame is garbbed from frame grabber class
    frame = frames.get_frame()
    # perspective projection is applied on the grabbed frame to re orient the image and extarct the ROI from image
    show_frame = cv2.warpPerspective(frame, perspectransform.transfmatrix, perspectransform.dim)
    # black pieces detction
    #Converting to HSV frame

    hsv = cv2.cvtColor(show_frame,cv2.COLOR_BGR2HSV)
    black_mask = cv2.inRange(hsv, black_lower, black_upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    black_mask = cv2.dilate(black_mask, kernel, iterations=2)

    # Checking if significant portion of skin is found in frame
    # converting the image into grayscale
    gray_frame = cv2.cvtColor(show_frame, cv2.COLOR_BGR2GRAY)
    # blurring the image with gaussian filter to remove noise
    gray_frame = cv2.GaussianBlur(gray_frame,G_kernel_size, 0)
    #sharpening the image for better edge detection
    gray_frame = sharpen_image(gray_frame)
    # Applying Canny Edge detection to detect the edges
    detected_edges = cv2.Canny(gray_frame, canny_l_threshold, canny_u_threshold)
    # dilating the image to make binary image more suitable for piece detection
    dilated = cv2.dilate(detected_edges, np.ones((19, 19)))

    if not skinDetector.check_skin(show_frame):
        board = [[0 for x in range(w)] for y in range(h)]

        for x in range(0, 8):
            for y in range(0, 8):
                index = 8*x + y

                text,isBlack = squares[index].check_square(show_frame,dilated,black_mask)

                if text == 0:
                    board[x][y] = text
                elif isBlack:
                    board[x][y] = "b"
                else:
                    board[x][y] = "w"

                cx, cy = squares[index].centroid
                cv2.circle(show_frame, (cx, cy), 5, (255, 0, 0), 3)

                #print(text)
                cv2.putText(show_frame, str(text), (cx, cy), font, 1, (255, 255, 255), 3)
                # Marking corners on the frame shown for each corner calculated with blue colored circles

        boardInterface.update(board)
    for j in pred_corners_list:
        x, y = j
        cv2.circle(show_frame, (x, y), 5, (0, 0, 255), -1)


    cv2.imshow('Chess Board', show_frame)
    cv2.imshow('Piece detection',dilated)
    cv2.imshow('Black Pieces',black_mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

