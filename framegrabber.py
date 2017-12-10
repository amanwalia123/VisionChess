from modules import *

class frame_grabber(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 1280)
        self.video.set(4, 1024)
        self.video.set(15, 0.8)
        self.reduceFactor = 2

    def __del__(self):
        self.video.release()

    def get_frame(self,redfactor=1):
        success, image = self.video.read()
        [height,width] = image.shape[0],image.shape[1]
        self.reduceFactor = redfactor
        image = cv2.resize(image,(width/self.reduceFactor,height/self.reduceFactor),interpolation=cv2.INTER_CUBIC)
        return image
