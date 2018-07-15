from abc import ABC, abstractmethod
from picamera.array import PiRGBArray
from time import sleep
from CameraHandler.Camera import Camera

import logging
import picamera.array


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
            self.camera.capture(rawCapture, format="bgr", use_video_port=False)
            image = rawCapture.array
            print("Image captured...")
            rawCapture.truncate(0)
            return image
            # print("Image size: ", image.nbytes/1024, "KB")
        except Exception as e:
            self.logger.error("Camera error: %s", e)

    @abstractmethod
    def test_drive(self):
        #Warm up the camera
        print("Warming up camera")
        sleep(2)
        for x in range(0, 10):
            img = self.capture()
            sleep(0.2)
            del img
        sleep(5)

    def adjust_camera(self, ldrValue):

        # To get iso: LDR / 6.25
        # To get Exposure: (ldr-5000)/200

        iso = 800
        exposure = 0

        if ldrValue >= 0:

            if ldrValue <= 312:
                iso = 50
            elif ldrValue > 10000:
                exposure = 25
                iso = 1600
            else:
                iso = round(ldrValue/6.25)
                exposure = round((ldrValue - 5000) / 200)

        self.camera.iso = iso
        self.camera.exposure_compensation = exposure

        print("ISO Value : ", iso)
        print("Current exposure_speed: ", self.camera.exposure_speed)
        sleep(0.5)

    def close_camera(self):
        self.camera.close()