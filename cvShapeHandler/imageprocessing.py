import cv2, imutils
import sys, datetime, pathlib
import numpy as np
import logging


class ImagePreProcessing:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def equaHist(img):
        # The code commented below only equalises the whole image and not piece by piece. This creates noise.
        # equ = cv2.equalizeHist(img)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        result = clahe.apply(img)
        return result

    @staticmethod
    def tobinnary(img):
        try:
            ret, img_bin = cv2.threshold(img, 127, 255, 0)
        except Exception:
            e = sys.exc_info()
            print(e)
            # self.logbook.error(e)
        return img_bin

    @staticmethod
    def togrey(img):
        try:
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            logging.error(e)
        return img_grey

    @staticmethod
    def get_histogram(img):
        return cv2.calcHist([img],[0],None,[256],[0,256])

    @staticmethod
    def adaptiveBinnary(img):
        t = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return t

    @staticmethod
    def tocanny(img, low_threshold):
        try:
            high_threshold = low_threshold * 2
            img_canny = cv2.Canny(img, low_threshold, high_threshold)
        except Exception as e:
            logging.error(e)
        return img_canny

    @staticmethod
    def denoise(img, intensity, search_window, block_size):
        try:
            denoise = cv2.fastNlMeansDenoising(img, intensity, search_window, block_size)
            #Usually searchWindows is 21 and blockSize is 7
        except Exception as e:
            logging.error(e)
        return denoise

    @staticmethod
    def blur(img, kernel_size=5, sigMaxX=0, sigMaxY=0):
        try:
            ksize = (kernel_size, kernel_size)
            blur = cv2.GaussianBlur(img, ksize, sigMaxX, sigMaxY)
        except Exception as e:
            logging.error(e)
        return blur

    @staticmethod
    def resize(img, newwidth):
        try:
            resized = imutils.resize(img, width=newwidth)
        except Exception as e:
            logging.error(e)
        return resized

    @staticmethod
    def cv_resize_compress(img, max_w=1640, max_h=1232, quality=80):
        try:
            img_h = img.shape[0]
            img_w = img.shape[1]
            new_h = img_h
            new_w = img_w

            print("Image current resolution: ", str(img_w), "x" , str(img_h))
            if img_w > max_w:
                new_w = max_w
                new_h = int((new_w * img_h)/img_w)
            
            if img_h > max_h:
                new_h = max_h
                
                new_w = int((new_h * img_w)/img_h)
  
            dist_size = (new_w, new_h)
            print("New size:", str(dist_size))
            resized = cv2.resize(img, dist_size, interpolation=cv2.INTER_AREA)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
            
            retval, buf = cv2.imencode('.jpg', resized, encode_param)
            return cv2.imdecode(buf, 1) #Flag 1 since it's colour
            
        except Exception as e:
            logging.error(e)

    @staticmethod
    def create_img(size):
        img = np.zeros((size[0], size[1], 4), np.uint8)
        return img

    @staticmethod
    def convert_img2bytes(img):
        bytes = cv2.imencode('.jpg', img)[1].tostring()
        return bytes

    def save(self, img):
        pathlib.Path('images').mkdir(parents=False, exist_ok=True)
        if img is not None:
            print("Saving image of", img.nbytes/10000000, "MB")
            try:
                tmp = ImagePreProcessing.cv_resize_compress(img)
                tmp = ImagePreProcessing.bgr2rgb(tmp)
                filename = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
                cv2.imwrite('images/'+filename+'.jpg', tmp)
            except Exception as e:
                self.logger.error(e)

    @staticmethod
    def rgb2bgr(img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    @staticmethod
    def bgr2rgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)