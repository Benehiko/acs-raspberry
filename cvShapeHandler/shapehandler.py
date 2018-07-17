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

        img_gray = ImagePreProcessing.togray(self.img)
        img_equ = ImagePreProcessing.equaHist(img_gray)
        img_morph = ImagePreProcessing.morph(img_equ)
        img_thresh = ImagePreProcessing.otsu_binary(img_morph)
        img_dilate = ImagePreProcessing.dilate(img_thresh)
        #img_canny = ImagePreProcessing.tocanny(img_dilate, 100)
        img_thresh = ImagePreProcessing.adaptiveBinnary(img_dilate)

        # OLD CODE
        # img_grey = ImagePreProcessing.togrey(self.img)
        #
        # img_thresh = ImagePreProcessing.tobinnary(img_grey)

        image, contours, hierarchy = cv2.findContours(img_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        self.contours = contours
        # cnts = contours[0] if imutils.is_cv2() else contours[1]
        return contours

    def polygontest(self, cnt_array, rect):
        count = 0
        ((x, y), (w, h), angle) = rect
        pnt_array = [(x, y), (x + w, y), (x, y - h), (x + w, y - h)]
        for cnt in cnt_array:
            for pnt in pnt_array:
                if cv2.pointPolygonTest(cnt, pnt, False) > -1:
                    count += 1
            if count == 4:
                rect_area = w * h  # cv2.contourArea(pnt_array)
                cnt_area = cv2.contourArea(cnt)
                if cnt_area > rect_area:
                    print("Point inside contour!")
                    return True
        return False

    def get_approx(self, cnt):
        epsilon = 0.01 * cv2.arcLength(cnt, False)
        approx = cv2.approxPolyDP(cnt, epsilon, False)
        return approx

    def get_rotated_rect(self, approx):
        rect = ((x, y), (w, h), angle) = cv2.minAreaRect(approx)
        return rect

    def in_scope_percentage(self, rect, area):
        ((x, y), (w, h), angle) = rect
        img_area, img_width, img_height = self.getAreaWidthHeight()
        p_a = (area * 100) / img_area
        p_w = w * 100 / img_width
        p_h = h * 100 / img_height
        if 0.15 <= p_a <= 1 and p_h <= 30 and p_w <= 30:
            if (0 >= angle >= -30 or -150 >= angle >= -180) or (0 <= angle <= 30 or 150 <= angle <= 180):
                return True
        return False

    def getRectangles(self, contours):

        arrrect = []
        cnt_cache = []
        for cnt in contours:
            # Contour
            approx = self.get_approx(cnt)

            area = cv2.contourArea(approx)
            rect = self.get_rotated_rect(approx)

            # Some calculations
            if self.in_scope_percentage(rect, area):
                cnt_cache.append(cnt)

        cnt_cache = [x for x in cnt_cache if
                     not self.polygontest(cnt_cache, self.get_rotated_rect(self.get_approx(x)))]  # Keep element if it is not False

        for cnt in cnt_cache:
            approx = self.get_approx(cnt)
            rect = self.get_rotated_rect(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            arrrect.append(box)

        return arrrect

    def isDuplicate(self, arrrect, box):
        for tmp in arrrect:
            return box == tmp

    def getAreaWidthHeight(self):
        print("DEBUG: Getting img area with shape property")
        imgHeight, imgWidth, imgChannels = self.img.shape
        imgArea = (imgHeight) * (imgWidth)
        return imgArea, imgWidth, imgHeight
