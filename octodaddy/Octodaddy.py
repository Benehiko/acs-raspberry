from Properties.applicationproperties import AppProperties
from backdrop.backdrop import Backdrop
from CameraHandler.piCam import PiCam
from CameraHandler.CameraProperties import CameraProperties
from time import sleep


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

    def run(self):
        while True:
            #Sameer enters check here for motion sensor
            # TODO:
            # ENTER THE MOTION DETECTION IF STATEMENT AND WRAP THE REST OF THE CODE IN IT

            #Do some camera stuff
            images = []
            for x in range(0, 5):
                images.append(self.camera.capture())
            #Get images and pass them to backdrop
            backdrop = Backdrop(self.app_properties, self, images=images)
            backdrop.run()
            self.backdrop_running = True
            sleep(15)

    def notify_backdrop(self):
        self.backdrop_running = False