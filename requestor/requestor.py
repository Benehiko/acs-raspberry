import netifaces
import requests
import logging
import socket


class Request:
    
    def __init__(self, url):
        self.url = url
        mac = netifaces.ifaddresses('eth0')[netifaces.AF_LINK]
        self.mac = mac[0].get('addr')
        self.logger = logging.getLogger(__name__)

    # http://docs.python-requests.org/en/latest/user/advanced/#post-multiple-multipart-encoded-files
    async def upload_data(self, multiple_files, backdrop):
        if not self.check_connectivity():
            self.logger.debug("Internet may be down...caching all images just in case for later.")
            backdrop.cache(multiple_files)
            return

        try:
            self.logger.info("Trying image upload...")
            data = [('mac', self.mac)]
            for file in multiple_files:
                data.append(('images', file, 'image/png'))
            return self.post(data)
        except Exception as e:
            self.logger.error("Error uploading image: %s", e)

    def post(self, data):
        try:
            self.logger.info("Posting data...")
            r = requests.post(self.url, files=data)
            self.logger.info("Server response: %s", r.text)
            print(r.text)
            print('Upload complete')
            return True
        except Exception as e:
            self.logger.error("Error on post: %s", e)
            return False

    def check_connectivity(self):
        conn = None
        try:
            conn = socket.create_connection(('google.com', 8080))
        except Exception as e:
            self.logger.log("Error contacting google server", e)
            return False
        finally:
            conn.close()

        return True
