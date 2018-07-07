from enum import Enum


class CameraResolutions(Enum):
    LOW = (640, 480)
    LOW_MEDIUM = (1280, 720)
    MEDIUM = (1920, 1080)
    MEDIUM_HIGH = (1640, 1232)
    HIGH = (3280, 2464)
