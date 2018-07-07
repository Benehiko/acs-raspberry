from Properties.applicationproperties import AppProperties
from backdrop.backdrop import Backdrop
from CameraHandler.piCam import PiCam
from CameraHandler.CameraProperties import CameraProperties


class Octodaddy:

    def __init__(self, app_properties, camera_properties):

        if isinstance(app_properties, AppProperties):
            self.app_properties = app_properties
            self.backdrop = Backdrop(app_properties, self)
        else:
            raise Exception("AppProperty type not found")

        if isinstance(camera_properties, CameraProperties):
            self.camera_properties = camera_properties

        self.backdrop_running = False

    def run(self):
        while True:
            pass
            #Check for light sensor

            #Do some camera stuff
            camera = PiCam(self.camera_properties)
            images = camera.capture()
            #Get images and pass them to backdrop
            self.backdrop.set_images(images=images)
            self.backdrop.run()
            self.backdrop_running = True

    def notify_backdrop(self):
        self.backdrop_running = False