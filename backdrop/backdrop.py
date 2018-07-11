from cvShapeHandler.process import Process
from requestor.requestor import Request
from PIL import Image
from io import BytesIO

import threading
import logging
import asyncio
import glob
import os
import datetime


class Backdrop(threading.Thread):

    def __init__(self, app_properties, octodaddy, images):
        threading.Thread.__init__(self)
        self.loop = None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.always_save = app_properties.get_always_save()
        self.save_drawn = app_properties.get_save_drawn()
        self.show_drawn = app_properties.get_show_drawn()
        self.no_network = app_properties.network_status()
        self.requestor = Request(app_properties.get_post_url())

        self.images = images
        self.octodaddy = octodaddy

    def run(self):
        self.loop = asyncio.new_event_loop()
        tasks = []

        # Check cache
        cached = self.check_cache()
        if len(cached) > 0:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tasks.append(asyncio.ensure_future(self.upload(cached, timestamp), loop=self.loop))

        images = self.images
        tasks.append(asyncio.ensure_future(self.process(images), loop=self.loop))
        self.loop.run_until_complete(asyncio.gather(*tasks))
        self.octodaddy.notify_backdrop()

    def cache(self, images):
        if len(images) > 0:
            for image in images:
                p = Process(img=image, resize=False, draw_enable=self.save_drawn, show_image=self.show_drawn)
                p.save()
                del p

    async def upload(self, images, timestamp):
        if len(images) > 0:
            self.logger.info("Queueing image upload")
            asyncio.ensure_future(self.requestor.upload_data(images, self, timestamp), loop=self.loop)

    def check_cache(self):
        cached_images = []
        images = glob.glob("images/*.jpg")
        for image in images:
            with open(image, 'rb') as file:
                image = Image.open(file)
                cached_images.append(image)
                # os.remove(image)
        return cached_images

    async def process(self, images):
        coros = []
        for image in images:
            p = Process(img=image, draw_enable=self.save_drawn, show_image=self.show_drawn, capture_handler=self)
            coros.append(p.process())

        results = await asyncio.gather(*coros)
        print("Length of array before extracting None types:", len(results))
        results = [x for x in results if x is not False] # Keep element if it is not False

        # tmp = []
        # for result in results:
        #     if result is not False:
        #         tmp.append(result)

        # del results

        print("Length of array after extracting None types:", len(results))
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await self.upload(results, timestamp)
