from cvShapeHandler.imageprocessing import ImagePreProcessing

import logging
import numpy as np
import cv2


class ShapeHandler:

    def __init__(self, img):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.img = img
        self.contours = None

    def findcontours(self):

        # Pre-process image
        # NEW CODE

        img_grey = ImagePreProcessing.togrey(self.img)


        img_equ = ImagePreProcessing.equaHist(img_grey)

        img_canny = ImagePreProcessing.tocanny(img_equ, 100)

        img_thresh = ImagePreProcessing.adaptiveBinnary(img_canny)

        # OLD CODE
        # img_grey = ImagePreProcessing.togrey(self.img)
        #
        # img_thresh = ImagePreProcessing.tobinnary(img_grey)

        image, contours, hierarchy = cv2.findContours(img_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        self.contours = contours
        # cnts = contours[0] if imutils.is_cv2() else contours[1]
        return contours

    def getRectangles(self, contours):
        arrrect = []
        imgArea = self.getArea()

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, False)
            approx = cv2.approxPolyDP(cnt, epsilon, False)
            area = cv2.contourArea(approx)
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            percentage = (area * 100) / imgArea
            if 0.2 < percentage < 20:
                arrrect.append(box)
        return arrrect

    def isDuplicate(self, arrrect, box):
        for tmp in arrrect:
            return box == tmp

    def getArea(self):
        print("DEBUG: Getting img area with shape property")
        imgHeight, imgWidth, imgChannels = self.img.shape
        imgArea = (imgHeight) * (imgWidth)
        return imgArea
