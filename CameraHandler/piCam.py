from abc import ABC, abstractmethod
from picamera.array import PiRGBArray
from time import sleep
<<<<<<< Updated upstream
=======
from CameraHandler.Camera import Camera
>>>>>>> Stashed changes

import logging
import picamera.array


class PiCam(Camera):

    def __init__(self, camera_properties):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.sensor = camera_properties.get_sensor_mode()
        self.camera_resolution = camera_properties.get_resolution()
        self.camera_framerate = camera_properties.get_framerate()

        self.camera = picamera.PiCamera(sensor_mode=self.sensor, resolution=self.camera_resolution.value, framerate=self.camera_framerate)

        self.test_drive()

    @abstractmethod
    def capture(self):

        rawCapture = PiRGBArray(self.camera)
        try:
            #Changing between bgr -> rgb (although opencv wants bgr)
            self.camera.capture(rawCapture, format="bgr", use_video_port=False)
            image = rawCapture.array
            print("Image captured...")

            # print("Image size: ", image.nbytes/1024, "KB")
        except Exception as e:
            self.logger.error("Camera error: %s", e)
        finally:
            rawCapture.truncate(0)
            return image

    @abstractmethod
    def test_drive(self):
        #Warm up the camera
        sleep(10)
        for x in range(0, 10):
            img = self.capture()
            del img

    def adjust_camera(self, ldrValue):

        lowLdr = 400
        medLowLdr = 500
        mediumLdr = 800
        medHighLdr = 1000
        highLdr = 1600

        low = 25000
        lowmed = 35000
        med = 50000
        medhigh = 70000
        high = 100000000

        #TODO: Call the LDR here to check the light intensity
<<<<<<< Updated upstream

        light_intensity = 500000
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
=======
        if ldrValue < 1000:
            self.camera.iso = lowLdr
            self.camera.shutter_speed = low
            print("isoValue : " + str(lowLdr))
            print("Shutter Speed : " + str(low))
            print("low")
        elif ldrValue > 1000 and ldrValue < 3000:
            self.camera.iso = medLowLdr
            self.camera.shutter_speed = lowmed
            print("isoValue : " + str(medLowLdr))
            print("Shutter Speed : " + str(lowmed))
            print("medlow")
        elif ldrValue > 3000 and ldrValue < 6000:
            self.camera.iso = mediumLdr
            self.camera.shutter_speed = med
            print("isoValue : " + str(mediumLdr))
            print("Shutter Speed : " + str(med))
            print("med")
        elif ldrValue > 6000 and ldrValue < 10000:
            self.camera.iso = medHighLdr
            self.camera.shutter_speed = medhigh
            print("isoValue : " + str(medHighLdr))
            print("Shutter Speed : " + str(medhigh))
            print("medhigh")
        elif ldrValue > 10000:
            self.camera.iso = highLdr
            self.camera.shutter_speed = high
            print("isoValue : " + str(highLdr))
            print("Shutter Speed : " + str(high))
            print("high")
        print("ldrValue : " + str(ldrValue))
        sleep(0.2)
>>>>>>> Stashed changes

    def close_camera(self):
        self.camera.close()