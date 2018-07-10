from cvShapeHandler.imageprocessing import ImagePreProcessing

import sys
import numpy as np
import cv2


class ShapeHandler:

    def __init__(self, img):
        # self.logbook = Logbook(self.__class__.__name__, 'cvShapeHandler')

        self.img = img
        self.contours = None

    def findcontours(self):
        # self.logbook.info("Inside findcontours Contours...")
        # Pre-process image
        img_grey = ImagePreProcessing.togrey(self.img)
        # self.logbook.info("Success on converting image to greyscale")

        img_equ = ImagePreProcessing.equaHist(img_grey)

        img_canny = ImagePreProcessing.tocanny(img_equ, 100)

        img_thresh = ImagePreProcessing.adaptiveBinnary(img_canny)

        # img_thresh = ImagePreProcessing.tobinnary(img_grey)
        # self.logbook.info("Success on converting image to binary")

        # self.logbook.info("Finding contours...")
        image, contours, hierarchy = cv2.findContours(img_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # self.logbook.info("Contours found: " + str(len(contours)))

        self.contours = contours
        # cnts = contours[0] if imutils.is_cv2() else contours[1]
        return contours

    def getRectangles(self, contours):
        arrrect = []
        imgArea = self.getArea()
        # self.logbook.info("Image Area is: " + str(imgArea))

        approxCounter = 0
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            approxCounter += 1

            if len(approx) == 4:
                area = cv2.contourArea(cnt)
                if area > 0:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    percentage = (area * 100) / imgArea
                    if percentage > 0.2:
                        arrrect.append(box)

        return arrrect

    def isDuplicate(self, arrrect, box):
        for tmp in arrrect:
            return box == tmp

    def getArea(self):
        imgHeight, imgWidth, imgChannels = self.img.shape
        imgArea = (imgHeight) * (imgWidth)
        return imgArea
