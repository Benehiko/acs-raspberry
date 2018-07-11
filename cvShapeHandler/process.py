from cvShapeHandler.imageprocessing import ImagePreProcessing
from cvShapeHandler.shapehandler import ShapeHandler
from cvShapeHandler.imagedraw import ImageDraw
from cvShapeHandler.imagedisplay import ImageDisplay
from cvShapeHandler.numpyencoder import NumpyEncoder

import logging
<<<<<<< Updated upstream
=======
import json
>>>>>>> Stashed changes


class Process:

    def __init__(self, img, resize=False, draw_enable=False, show_image=False, capture_handler=None):
        self.logger = logging.getLogger(self.__class__.__name__)

        # Captured image is rgb, convert to bgr
        self.img = img  # ImagePreProcessing.rgb2bgr(img)
        self.imgShapeH = None
        self.draw_enable = draw_enable
        self.show_image = show_image
        self.resize = resize
        self.capture_handler = capture_handler

    async def process(self):
        # Resize image
        img = self.img.copy()
        if self.resize:
            img = ImagePreProcessing.resize(img, 1080)
            # ratio = img.shape[0] / float(resized.shape[0])

        self.imgShapeH = ShapeHandler(img)
        contours = self.imgShapeH.findcontours()
        if len(contours) > 0:

            rectangles = self.imgShapeH.getRectangles(contours)

            if len(rectangles) > 0:
                if self.draw_enable:
                    try:
                        img = ImageDraw.draw(img, rectangles, "Green", 10)
                    except Exception as e:
                        self.logger.error(e)
                    self.save(image=img)
                    if self.show_image:
                        ImageDisplay.display(img)

                # self.overlay_handler(rectangles)
                print("Image has rectangles!")
                jrect = self.rectangle2json(rectangles)
                img_list = ImagePreProcessing.crop(self.img, jrect)
                return self.img

        return False

    def rectangle2json(self, rectangles):
        inner = {'rectangles': {}}
        counter = 0
        for rectangle in rectangles:
            inner['rectangles'][counter] = NumpyEncoder().default(rectangle)
            counter += 1

        j = json.dumps(inner)
        return j

    def overlay_handler(self, rectangles):
        h, w, c = self.img.shape
        layer1 = Process.create_transparent_img(size=(h, w))  # opencv height then width
        res = layer1[:]
        layer2 = ImageDraw.draw(res, rectangles, "Green", 10)
        cnd = layer2[:, :, 3] > 0
        res[cnd] = layer2[cnd]
        res = ImagePreProcessing.cv_resize_compress(res, max_w=1280, max_h=960)
        height, width, channels = res.shape
        b = ImagePreProcessing.convert_img2bytes(res)
        self.capture_handler.add_overlay(img_bytes=b, size=(width, height))

    def save(self, image=None):
        try:
            if image is not None:
                ImagePreProcessing.save(image)
            else:
                ImagePreProcessing.save(self.img)
        except Exception as e:
            self.logger.error(e)

    @staticmethod
    def compress(image):
        try:
            if image is not None:
                return ImagePreProcessing.cv_resize_compress(image)
            else:
                return None
        except Exception as e:
            logging.error(e)

    @staticmethod
    def normalise_image(image):
        try:
            if image is not None:
                return ImagePreProcessing.bgr2rgb(image)
            else:
                return None
        except Exception as e:
            logging.error(e)

    @staticmethod
    def create_transparent_img(size=(960, 1280)):
        return ImagePreProcessing.create_img(size=size)  # Opencv prefers Height and then Width thus (h,w)
