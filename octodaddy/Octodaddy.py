from Properties.applicationproperties import AppProperties
from backdrop.backdrop import Backdrop
from CameraHandler.piCam import PiCam
from CameraHandler.CameraProperties import CameraProperties
from time import sleep
from Sensors.ldrTest import ldr
from Sensors.ledFlash import flashLight

# import RPi.GPIO as GPIO

import time
import sys


class Octodaddy:

    def __init__(self, app_properties, camera_properties):

        if isinstance(app_properties, AppProperties):
            self.app_properties = app_properties

        else:
            raise Exception("AppProperty type not found")

        if isinstance(camera_properties, CameraProperties):
            self.camera_properties = camera_properties

        self.camera = PiCam(self.camera_properties)
        self.backdrop_running = False

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # self.pinpir = 22
        # GPIO.setup(self.pinpir, GPIO.IN)

    def run(self):

        while True:

            # Loops through the sensor infinitely to check for motion, once detected, set iso and shutter and capture images

            currentstate = 1
            previousstate = 0

            try:
                print('waiting for pir to settle...')
                # Loop until PIR output is 0
                # while GPIO.input(self.pinpir) == 1:
                #     currentstate = 0

                print("    ready")
                # Loop until user quits with control C
                while True:
                    # Read PIR state

                    # currentstate = GPIO.input(self.pinpir)

                    # If PIR is triggered
                    if currentstate == 1 and previousstate == 0:
                        print("motion detected")
                        flashLight._flashLight()
                        # setting iso and shutterspeed
                        ldrValue = 3100  # ldr.readldr()
                        self.camera.adjust_camera(ldrValue)

                        images = []
                        for x in range(0, 5):
                            images.append(self.camera.capture())
                            sleep(0.3)

                        # Get images and pass them to backdrop
                        backdrop = Backdrop(self.app_properties, self, images=images)
                        backdrop.start()
                        self.backdrop_running = True
                        sleep(5)
                        # record previous state of motion detector
                        previousstate = 0
                    # If the PIR has returned to ready state
                    elif currentstate == 0 and previousstate == 1:
                        print("     ready")
                        previousstate = 0

                    time.sleep(5)

            except KeyboardInterrupt:
                print("     Quit")
                sys.exit(0)
                # GPIO.cleanup()

    def notify_backdrop(self):
        self.backdrop_running = False
