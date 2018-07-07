from cvShapeHandler.process import Process
from requestor.requestor import Request
from PIL import Image

import threading
import logging
import asyncio
import glob
from io import BytesIO


class Backdrop(threading.Thread):

    def __init__(self, app_properties, octodaddy):
        threading.Thread.__init__(self)
        self.loop = None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.always_save = app_properties.get_always_save()
        self.save_drawn = app_properties.get_save_drawn()
        self.show_drawn = app_properties.get_show_drawn()
        self.no_network = app_properties.network_status()
        self.requestor = Request(app_properties.get_post_url())

        self.images = None
        self.octodaddy = octodaddy

    def set_images(self, images):
        self.images = images

    def run(self):
        self.loop = asyncio.new_event_loop()
        tasks = []

        #Check cache
        cached = self.check_cache()
        if len(cached) > 0:
            tasks.append(asyncio.ensure_future(self.upload(cached)))

        images = self.images
        tasks.append(asyncio.ensure_future(self.process(images)))
        self.loop.run_until_complete(asyncio.gather(*tasks))
        self.octodaddy.notify_backdrop()

    def cache(self, images):
        if len(images) > 0:
            for image in images:
                p = Process(img=image, resize=False, draw_enable=self.save_drawn, show_image=self.show_drawn)
                p.save()
                del p

    async def upload(self, images):
        if len(images) > 0:
            tmp_img = []
            for image in images:
                tmp_img = Process.compress(image)
                self.logger.info("Queueing image upload")

            asyncio.ensure_future(self.requestor.upload_data(tmp_img, self))

    def check_cache(self):
        cached_images = []
        images = glob.glob("images/*.jpg")
        for image in images:
            with open(image, 'rb') as file:
                image = Image.open(file)
                cached_images.append(image)
        return cached_images

    async def process(self, images):
        coros = []
        for image in images:
            p = Process(img=image, draw_enable=self.save_drawn, show_image=self.show_drawn, capture_handler=self)
            coros.append(p.process())

        results = await asyncio.gather(*coros)
        print("Length of array before extracting None types: %d", len(results))
        # results = [x for x in results if x is not None] # Keep element if it is not None
        tmp_images = []
        for result in results:
            if result is not False:
                image = Image.fromarray(result)
                tmp = BytesIO()
                image.save(tmp, "JPEG")
                tmp.seek(0)
                tmp_images.append(result)

        await self.upload(tmp_images)