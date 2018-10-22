from CameraHandler.cameraresolutions import CameraResolutions
from Properties.applicationproperties import AppProperties
from CameraHandler.CameraProperties import CameraProperties
from octodaddy.Octodaddy import Octodaddy

import argparse
import os, logging.config, json


def setup_logging(default_path='logsettings.json', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


url_old = 'http://104.40.251.46:8081/OcrRest/webapi/ocr/pic/pi'
url = 'http://41.188.221.238:8081/ocr/pic/pi'
url_local = 'http://192.168.0.109:8080/webapi/ocr/multi/pi'

ap = argparse.ArgumentParser(description='Plateos version 3.4')
ap.add_argument("-u", "--url", required=False, help="enter the url to override the default url")
ap.add_argument("-cp", "--camera_preview_on", action="store_true", required=False,
                help="Enable the camera preview screen. Please note that if the resolution is set to a high amount the screen will start flashing on image captures...")
ap.add_argument("-cr", "--camera_resolution", type=int, required=False,
                help="Set the camera resolution from mode (1 - 5). 5 being the highest")
ap.add_argument("-cfr", "--camera_frame_rate", type=float, required=False,
                help="Set the camera frame rate. Do take note some resolution settings only support certain frame rates")
ap.add_argument("-cs", "--camera_sensor", type=int, required=False,
                help="The camera_resolution param overrides this param. There are 1-7 options. Please check this resources for more information:http://picamera.readthedocs.io/en/release-1.10/fov.html#camera-modes")
ap.add_argument("-sa", "--save_images_always", action="store_true", required=False,
                help="Always save the image if true")
ap.add_argument("-sd", "--save_images_drawn", action="store_true", required=False,
                help="Save images with drawn shapes")
ap.add_argument("-shd", "--show_drawn", action="store_true", required=False, help="Show all drawn images")
ap.add_argument("-cl", "--capture_limit", type=int, required=False, help="Set the capture limit per cycle")
ap.add_argument("-n", "--no_network", action="store_true", required=False, help="Simulate no network")
args, leftovers = ap.parse_known_args()

if args.url is not None:
    print("Changed url to", args.url)
    url = args.url

# Setting Camera Preview
if args.camera_preview_on is not False:
    print("Setting camera_preview on")
    camera_preview = True
else:
    camera_preview = False

# Setting Camera Resolution
if args.camera_resolution is not None:
    print("Setting camera_resolution to ", args.camera_resolution)
    camera_resolution = args.camera_resolution
    if camera_resolution == 1:
        camera_resolution = CameraResolutions.Low
    elif camera_resolution == 2:
        camera_resolution = CameraResolutions.LOW_MEDIUM
    elif camera_resolution == 3:
        camera_resolution = CameraResolutions.MEDIUM
    elif camera_resolution == 4:
        camera_resolution = CameraResolutions.MEDIUM_HIGH
    elif camera_resolution == 5:
        camera_resolution = CameraResolutions.HIGH
else:
    camera_resolution = CameraResolutions.HIGH

# Setting Camera Frame Rate
if args.camera_frame_rate is not None:
    print("Setting camera_frame_rate to ", args.camera_frame_rate)
    camera_frame_rate = args.camera_frame_rate
else:
    camera_frame_rate = 5

# Setting Camera Sensor
if args.camera_sensor is not None:
    print("Setting camera_sensor to", args.camera_sensor)
    camera_sensor = args.camera_sensor
else:
    camera_sensor = 2

# Setting Always Save Image
if args.save_images_always is not False:
    print("Setting save_images_always on")
    save_image = True
else:
    save_image = False

# Setting Save Drawn Images
if args.save_images_drawn is not False:
    print("Setting save_images_drawn on")
    save_drawn = True
else:
    save_drawn = False

# Show Drawn Images
if args.show_drawn is not False:
    print("Setting show_drawn on")
    show_drawn = True
else:
    show_drawn = False

# Setting Capture Limit
if args.capture_limit is not None:
    print("Setting capture_limit ", args.capture_limit)
    capture_limit = args.capture_limit
else:
    capture_limit = 5

# Setting No network simulation
if args.no_network is not False:
    print("Setting no network to on")
    no_network = True
else:
    no_network = False

print("Starting Plateos version 4")
setup_logging()
print("Setting Application Properties")
appProperties = AppProperties(no_network=no_network, save_drawn=save_drawn, show_drawn=show_drawn,
                              always_save=save_image, camera_preview=camera_preview, capture_limit=capture_limit,
                              post_url=url)
print("Setting Camera Properties")
cameraProperties = CameraProperties(sensor_mode=camera_sensor, resolution=camera_resolution, framerate=camera_frame_rate)
octo = Octodaddy(app_properties=appProperties, camera_properties=cameraProperties)
print("Starting programme")
octo.run()
