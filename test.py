from cvShapeHandler.shapehandler import ShapeHandler
from cvShapeHandler.imagedraw import ImageDraw
from cvShapeHandler.imagedisplay import ImageDisplay
from requestor.requestor import Request

import cv2
import glob

images = glob.glob('site/*.jpg')
request = Request("http://localhost:8080/webapi/ocr/multi/pi")
count = 0

multi = []

for image in images:
    if count == 5:
        count = 0
        request.upload_data(multi, "something")
        multi.clear()

    img = cv2.imread(image)
    multi.append(img)
    count = count + 1

    # s = ShapeHandler(img)
    # rectangles = s.getRectangles(s.findcontours())
    # ImageDraw.draw(img, rectangles, "GREEN", 5)
    # ImageDisplay.display(img)
