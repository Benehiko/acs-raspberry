from Properties.applicationproperties import AppProperties
from backdrop.backdrop import Backdrop
from CameraHandler.piCam import PiCam
from CameraHandler.CameraProperties import CameraProperties
from time import sleep
# from Sensors.ldrTest import ldr
# from Sensors.ledFlash import flashLight

# import RPi.GPIO as GPIO

import time
import sys
import gc
import logging
import datetime


class Octodaddy:

    def __init__(self, app_properties, camera_properties):

        self.logger = logging.getLogger(self.__class__.__name__)

        if isinstance(app_properties, AppProperties):
            self.app_properties = app_properties

        else:
            raise Exception("AppProperty type not found")

        if isinstance(camera_properties, CameraProperties):
            self.camera_properties = camera_properties
        else:
            raise Exception("Camera Properties not found")

        self.camera = PiCam(self.camera_properties)
        self.camera.test_drive()
        self.camera.close_camera()

        self.previous_ldr = 50 #ldr.readldr()

        # self.backdrop_running = False

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # self.pinpir = 22
        # GPIO.setup(self.pinpir, GPIO.IN)

    def run(self):

        # Loops through the sensor infinitely to check for motion, once detected, set iso and shutter and capture images

        currentstate = 1  # 0
        previousstate = 0

        try:
            print('waiting for pir to settle...')
            # Loop until PIR output is 0
            # while GPIO.input(self.pinpir) == 1:
            # currentstate = 0

            print("ready")
            # Loop until user quits with control C
            while True:
                # Read PIR state

                # currentstate = GPIO.input(self.pinpir)

                # If PIR is triggered
                if currentstate == 1 and previousstate == 0:
                    print("motion detected")
                    # flashLight._flashLight()

                    self.camera = PiCam(self.camera_properties)

                    # setting iso and shutterspeed
                    ldrValue = 300 # ldr.readldr()

                    change = (self.previous_ldr * 100) / ldrValue

                    if self.previous_ldr < 1:
                        self.previous_ldr = ldrValue
                        self.camera.adjust_camera(ldrValue)

                    elif change > 10:
                        self.previous_ldr = ldrValue
                        self.camera.adjust_camera(ldrValue)

                    images = []
                    for x in range(0, 3):
                        images.append(self.camera.capture())
                        sleep(0.3)

                    self.camera.close_camera()
                    del self.camera

                    # Get images and pass them to backdrop
                    backdrop = Backdrop(self.app_properties)
                    backdrop.set_images(images)
                    backdrop.start()
                    # self.backdrop_running = True
                    # record previous state of motion detector
                    previousstate = 0  # 1
                # If the PIR has returned to ready state
                elif currentstate == 0 and previousstate == 1:
                    print("ready")
                    previousstate = 0

                time.sleep(30)

        except KeyboardInterrupt as e:
            self.logger.error(e)
            # GPIO.cleanup()
            sys.exit(0)

    def notify_backdrop(self, start_time):
        gc.collect()
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info("Thread started on: %s",start_time)
        self.logger.info("Thread ended on: %s",end_time)
        # self.backdrop_running = False
