import RPi.GPIO as GPIO
import time

class WindowSensorInterface:
    inputPin = 24
    terminate = False
    alarmTripStatus = False
    
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input
        print("Initialized Window Sensor")
    
    def test(self):
        testInput = GPIO.input(self.inputPin) #0 = window closed, 1 = window open
        print(testInput)
        
    def runSensor(self):
        trippedCounter = 0
        while not self.terminate:
            sensorInput = GPIO.input(self.inputPin)
            print('Window Sensor: ' + str(sensorInput))
            
            if(sensorInput == 1):
                trippedCounter += 1
            else:
                trippedCounter = 0
                
            if(trippedCounter > 3):
                self.alarmTripStatus = True
            else:
                self.alarmTripStatus = False
            time.sleep(.1)
            
    def shutdown(self):
        self.terminate = True

    def alarmTripped(self):
        return self.alarmTripStatus