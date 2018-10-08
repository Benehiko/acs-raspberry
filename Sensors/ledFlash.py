import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)

class flashLight:
    
    def _flashLight():
        print("Light on")
        GPIO.output(18, GPIO.HIGH)

        time.sleep(0.1)

        print("Light off")
        GPIO.output(18, GPIO.LOW)

        #GPIO.cleanup(18)
