import RPi.GPIO as GPIO
import time

class MotionSensorInterface:
    inputPin = 23
    terminate = False
    alarmTripStatus = False
        
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input
        print("Initialized Motion Sensor")
    
    def test(self):
        testInput = GPIO.input(self.inputPin) #0 = window closed, 1 = window open
        print(testInput)
        
    def runSensorInterface(self):
        trippedCounter = 0
        initializedCount = 0
        initialized = False
        while not self.terminate:
            sensorInput = GPIO.input(self.inputPin)
            #print('Motion Sensor: ' + str(sensorInput))
            
            if(not initialized):
                if(sensorInput == 1):
                    initializedCount += 1
                if(initializedCount > 20):
                    initialized = True
                    print("Motion Sensor Initialized")
            
            elif(sensorInput == 0):
                trippedCounter += 1
            else:
                trippedCounter = 0
                
            #print("MS TRIP COUNT: " + str(trippedCounter))
            if(trippedCounter > 3):
                print("MS TRIPPED")
                self.alarmTripStatus = True
            elif(self.alarmTripStatus == True):
                print("MS RESET")
                self.alarmTripStatus = False
            time.sleep(.1) #check at 10 Hz
        print("Motion Sensor Shutdown Complete")
            
    def shutdown(self):
        print("Shutting Down Motion Sensor")
        self.terminate = True
        
    def alarmTripped(self):
        return self.alarmTripStatus
            
