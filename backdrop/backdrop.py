from cvShapeHandler.process import Process
from requestor.requestor import Request
from PIL import Image

import os
import threading
import logging
import asyncio
import glob
import datetime


class Backdrop(threading.Thread):

    def __init__(self, app_properties):
        threading.Thread.__init__(self)

        self.loop = None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.always_save = app_properties.get_always_save()
        self.save_drawn = app_properties.get_save_drawn()
        self.show_drawn = app_properties.get_show_drawn()
        self.no_network = app_properties.network_status()
        self.requestor = Request(app_properties.get_post_url())

        # self.images = images
        # for tmp in images:
        #     self.images.append(Process.rgb2bgr(tmp))

        #self.octodaddy = octodaddy
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_images(self, images):
        self.images = images

    def run(self):
        self.loop = asyncio.new_event_loop()
        tasks = []

        # Check cache
        # cached = self.check_cache()
        # if len(cached) > 0:
        #     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     tasks.append(asyncio.ensure_future(self.upload(cached, timestamp), loop=self.loop))

        images = self.images

        if self.always_save:
            self.cache(images)

        tasks.append(asyncio.ensure_future(self.process(images), loop=self.loop))
        self.loop.run_until_complete(asyncio.gather(*tasks, loop=self.loop))
        #self.octodaddy.notify_backdrop(self.start_time)

    def cache(self, images):
        if len(images) > 0:
            for image in images:
                #p = Process(img=image, resize=False, draw_enable=self.save_drawn, show_image=self.show_drawn)
                Process.save("cache", image)

    async def upload(self, images, timestamp):
        if len(images) > 0 and not self.no_network:
            self.logger.info("Queueing image upload")
            asyncio.ensure_future(self.requestor.upload_data(images, self, timestamp), loop=self.loop)

    def check_cache(self):
        cached_images = []
        images = glob.glob("cache/*.jpg")
        for image in images:
            with open(image, 'rb') as file:
                image = Image.open(file)
                cached_images.append(image)
                os.remove(image)
        return cached_images

    async def process(self, images):
        coros = []
        for image in images:
            p = Process(img=image, draw_enable=self.save_drawn, show_image=self.show_drawn, resize=False)
            coros.append(p.process())

        results = await asyncio.gather(*coros, loop=self.loop)
        print("Length of array before extracting None types:", len(results))
        results = [x for x in results if x is not False] # Keep element if it is not False

        print("Length of array after extracting None types:", len(results))
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await self.upload(results, timestamp)
