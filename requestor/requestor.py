import json
from urllib.request import urlopen

import netifaces
import requests
import logging
import socket
import datetime
from PIL import Image
from io import BytesIO
from cvShapeHandler.process import Process


class Request:

    def __init__(self, url):
        self.url = url
        mac = netifaces.ifaddresses('eth0')[netifaces.AF_LINK]
        self.mac = mac[0].get('addr')
        self.logger = logging.getLogger(__name__)

    # http://docs.python-requests.org/en/latest/user/advanced/#post-multiple-multipart-encoded-files
    async def upload_data(self, multiple_files, timestamp):
        if len(multiple_files) > 0:
            if not self.check_connectivity():
                print("Internet down")
                self.logger.debug("Internet may be down...caching all images just in case for later.")
                # backdrop.cache(multiple_files)
                return

            try:
                data = [('mac', self.mac), ('timestamp', timestamp)]
                counter = 0
                for i in multiple_files:
                    nparray = Process.compress(i)
                    if nparray is not None:
                        image = Image.fromarray(nparray)
                        tmp = BytesIO()
                        image.save(tmp, "JPEG")
                        tmp.seek(0)
                        data.append(('images', (str(counter)+'.png', tmp, 'image/png')))
                        counter = counter + 1

                print("Trying upload", data)
                self.logger.info("Trying image upload...")
                return self.post(data)
            except Exception as e:
                self.logger.error("Error uploading image: %s", e)
        return

    def post(self, data):
        try:
            self.logger.info("Posting data...")
            r = requests.post(self.url, files=data)
            print(r.text)
            self.logger.info("Server response: %s", r.text)
            print('Upload complete')
            return True
        except Exception as e:
            self.logger.error("Error on post: %s", e)
            return False

    def check_connectivity(self):
        try:
            urlopen('http://google.com', timeout=3)
            return True
        except Exception as e:
            print("Testing google ping", e)
            pass

        return False
