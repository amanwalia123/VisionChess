from modules import *


class ChessSquare(object):


    def __init__(self,coord,pts,init_frame,white_count_thresh,black_piece_thresh):
        #chess sqaure cartesian coordinate
        self.coordinate = coord

        #Four points associated with this square
        self.points = pts

        #centroid of this square
        self.centroid = np.asarray((sum(np.asarray(pts))/4), dtype=np.int)


        #Store initial square coordinates
        self.init_square = self.crop_square(init_frame, self.points)
        self.init_square_gray = cv2.cvtColor(self.init_square, cv2.COLOR_BGR2GRAY)

        #whether a chess square is filled or not
        self.filled = False

        #thresholding parameters
        self.white_count_thresh = white_count_thresh
        self.black_piece_thresh = black_piece_thresh

        #name = "Coordinate #"+str(self.coordinate)
        #cv2.imshow(name,self.init_sqr)

    def name(self):
        return str(self.coordinate)

    def show_square(self, image_frame):
        return self.crop_square(image_frame, self.points)

    def crop_square(self,frame,coordinates):
        # image of initial square of the chess board
        # top leftcorner
        (x1, y1) = coordinates[0]
        # bottom right corner
        (x3, y3) = coordinates[2]
        return frame[y1:y3, x1:x3]

    def check_square(self,image_frame,canny_image,black_mask):

        # getting width of the square
        sq_width = abs((self.points[3,:]-self.points[0,:])[0])
        (cx,cy) = self.centroid - self.points[0,:]
        perc_area =  0.50
        thres_square_dim = int(sq_width*0.4)
        
        #cropping the square for
        curr_square = self.crop_square(canny_image,self.points)
        black_piece = self.crop_square(black_mask, self.points)
        count_canny = 0
        count_black_piece = 0
        for i in range(cx-thres_square_dim/2,cx+thres_square_dim/2):
            for j in range(cy-thres_square_dim/2,cy+thres_square_dim/2):
                if curr_square[i,j] == 255:
                    count_canny += 1
                if black_piece[i,j] == 255:
                    count_black_piece += 1

        if count_canny > self.white_count_thresh:
            canny_piece_detected = True
        else:
            canny_piece_detected = False

        if count_black_piece > self.black_piece_thresh:
            black_piece_detected = True
        else:
            black_piece_detected = False

        if canny_piece_detected and not black_piece_detected:
            return (1, False)
        elif black_piece_detected:
            return (1, True)
        else:
            return (0, False)

    def background_sub(self,image_frame):
        curr_square = self.crop_square(image_frame, self.points)
        curr_square_gray = cv2.cvtColor(curr_square, cv2.COLOR_BGR2GRAY)
        sub = cv2.subtract(self.init_square_gray,curr_square_gray)
        return sub




