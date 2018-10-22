import asyncio
import datetime
from requestor.requestor import Request

import cv2
import glob


async def test():
    images = glob.glob('site/*.jpg')
    print(images)
    request = Request("http://41.188.221.238:8081/ocr/pic/pi")

    multi = []
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for image in images:
        img = cv2.imread(image)
        multi.append(img)

    await request.upload_data(multi, timestamp)
    multi.clear()

        # s = ShapeHandler(img)
        # rectangles = s.getRectangles(s.findcontours())
        # ImageDraw.draw(img, rectangles, "GREEN", 5)
        # ImageDisplay.display(img)


loop = asyncio.get_event_loop()
task = asyncio.ensure_future(test(), loop=loop)
loop.run_until_complete(task)
