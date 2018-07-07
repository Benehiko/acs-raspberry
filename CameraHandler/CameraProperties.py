from CameraHandler.cameraresolutions import CameraResolutions


class CameraProperties:

    def __init__(self, stereo_mode=None, stereo_decimate=False, resolution=None, framerate=None, sensor_mode=2, led_pin=None, clock_mode='reset', framerate_range=None):

        if stereo_mode is not None:
            self.stereo_mode = stereo_mode

        if stereo_decimate is not None:
            self.stereo_decimate = stereo_decimate

        if resolution is not None:
            self.resolution = resolution

        if framerate is not None:
            self.framerate = framerate
        else:
            self.framerate = 15

        self.sensor_mode = sensor_mode

        if led_pin is not None:
            self.led_pin = led_pin

        self.clock_mode = clock_mode

        if framerate_range is not None:
            self.framerate_range = framerate_range
        else:
            self.framerate_range = (1, 15)

    def get_resolution(self):
        return self.resolution

    def set_resolution(self, resolution=CameraResolutions.HIGH):
        self.resolution = resolution

    def get_framerate(self):
        return self.framerate

    def set_framerate(self, framerate=15):
        self.framerate = framerate

    def get_framerate_range(self):
        return self.framerate_range

    def set_framerate_range(self, framerate_range=(1, 15)):
        self.framerate_range = framerate_range

    def get_sensor_mode(self):
        return self.sensor_mode

    def set_sensor_mode(self, sensor_mode=2):
        self.sensor_mode = sensor_mode

    def get_stereo_mode(self):
        return self.stereo_mode

    def set_stereo_mode(self, stereo_mode=None):
        self.stereo_mode = stereo_mode

    def get_stereo_decimate(self):
        return self.stereo_decimate

    def set_stereo_decimate(self, stereo_decimate=False):
        self.stereo_decimate = stereo_decimate

    def get_led_pin(self):
        return self.led_pin

    def set_led_pin(self, led_pin=None):
        self.led_pin = led_pin

    def get_clock_mode(self):
        return self.clock_mode

    def set_clock_mode(self, clock_mode='reset'):
        self.clock_mode = clock_mode

