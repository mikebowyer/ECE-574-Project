import RPi.GPIO as GPIO
import time

class WindowSensorInterface:
    inputPin = 24
    terminate = False
        
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input
        print("Initialized Window Sensor")
    
    def test(self):
        testInput = GPIO.input(self.inputPin) #0 = window closed, 1 = window open
        print(testInput)
        
    def runSensor(self):
        
        while not self.terminate:
            sensorInput = GPIO.input(self.inputPin)
            print('Window Sensor: ' + str(sensorInput))
            time.sleep(.2)
            
    def shutdown(self):
        self.terminate = True
            