import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinldr = 27

GPIO.setup(pinldr, GPIO.OUT)
GPIO.output(pinldr, GPIO.LOW)

lowLdr = 400
medLowLdr = 600
mediumLdr = 800
medHighLdr = 1000
highLdr = 1200


class ldr:

    def readldr():
        ldrcount = 0 #sets the count to 0

        
        time.sleep(0.1) #Drains all charge from the capacitor
        GPIO.setup(pinldr, GPIO.IN) #sets the pin to be input
        #While the input reads low or off, count
        while(GPIO.input(pinldr) == GPIO.LOW):
            ldrcount += 1
        return ldrcount
    
    def ldrConfig():

        ldrValue = self.readldr()
        result = 0
        
        if ldrValue < 500:
            result = lowLdr
            #self.camera.shutter_speed = 200000
            
        elif ldrValue > 500 and ldrValue < 1500:
            result = medLowLdr
            #self.camera.shutter_speed = 400000
            
        elif ldrValue > 1500 and ldrValue < 2500:
            result = mediumLdr
            #self.camera.shutter_speed = 500000
            
        elif ldrValue > 2500 and ldrValue < 3500:
            result = medHighLdr
            #self.camera.shutter_speed = 700000
            
        elif ldrValue > 3500:
            result = highLdr
            #self.camera.shutter_speed = 1000000
        something = str(result)    
        return something        
            
            
        

#while True:
#    print(readldr())
#    time.sleep(1)
    
    