from abc import ABC, abstractmethod
from picamera.array import PiRGBArray
from time import sleep

import logging
import picamera.array
import datetime

from CameraHandler.Camera import Camera


class PiCam(Camera):

    def __init__(self, camera_properties):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.sensor = camera_properties.get_sensor_mode()
        self.camera_resolution = camera_properties.get_resolution()
        self.camera_framerate = camera_properties.get_framerate()

        self.camera = picamera.PiCamera(sensor_mode=self.sensor, resolution=self.camera_resolution.value, framerate=self.camera_framerate)

    @abstractmethod
    def capture(self):

        rawCapture = PiRGBArray(self.camera)
        try:
            #Changing between bgr -> rgb (although opencv wants bgr)
            self.camera.capture(rawCapture, format="rgb", use_video_port=False)
            image = rawCapture.array

            # print("Image size: ", image.nbytes/1024, "KB")
        except Exception as e:
            self.logger.error("Camera error: %s", e)
        finally:
            del rawCapture
            return image

    @abstractmethod
    def test_drive(self):
        for x in range(0, 3):
            self.capture()
            sleep(1)

    def adjust_camera(self, light_intensity):

        now = datetime.datetime.now()
        today6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)


        mode = None
        if now < today6am or now > today5pm:
            print("Entering low light mode")
            self.camera.shutter_speed = 1500000
            self.camera.iso = 800
            mode = "night"
        else:
            print("Day mode")
            self.camera.shutter_speed = 800000
            self.camera.iso = 100
            mode = "day"

        # Stepping up from night mode (worst case to best case with light)
        if light_intensity in range(260000, 7000000):
            # Light is low (florescent or moonlight)
            # Set the camera to capture more light into the lense
            self.camera.iso = 1000
            self.camera.shutter_speed = 2500000

        elif light_intensity >= 12000000:
            if mode is "day":
                self.camera.iso = 50
                self.camera.shutter_speed = 500000
            elif mode is "night":
                self.camera.iso = 400
                self.camera.shutter_speed = 1000000