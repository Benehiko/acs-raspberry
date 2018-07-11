import RPi.GPIO as GPIO
import time
#import ledFlash
#import cameraCapture
#import _thread
from Sensors.ledFlash import flashLight

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinpir = 22

print("PIR Module Test (CTRL-C to exit)")

GPIO.setup(pinpir, GPIO.IN)



class _motionSensor:
    
    def detectMotion():

        try:
#            currentstate = 0
#            previousstate = 0
            
            print('waiting for pir to settle...')
            # Loop until PIR output is 0
#            while GPIO.input(pinpir) == 1:
#                currentstate = 0
                
#            print("    ready")
            #Loop until user quits with control C
#            while True:
                #Read PIR state
            currentstate = GPIO.input(pinpir)
            currentstate1 = str(currentstate)
            print("Current state is " + currentstate1)    
                #If PIR is triggered
            if currentstate == 1:
                print("motion detected")
                flashLight._flashLight()
                return True
            else:
                return False
                #_thread.start_new_thread(cameraCapture.capture, ())
                #record previous state
                #previousstate = 1
            #If the PIR has returned to ready state
#            elif currentstate == 0 and previousstate == 1:
#                print("     ready123")
#                previousstate = 0

#            time.sleep(0.01)
            
            #return True
                
        except KeyboardInterrupt:
            print("     Quit")
            
            #Reset GPIO settings
            GPIO.cleanup()
