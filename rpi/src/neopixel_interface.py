import board
import neopixel

import time
import random

class NeopixelInterface:
    pixels = None
    terminate = False
    currentLightMode = "NONE"
    customBlue = 0
    customGreen = 0
    customRed = 0
    def init(self):
        self.pixels = neopixel.NeoPixel(board.D21, 12)
        #self.pixels.fill((127, 127, 127))
        #self.pixels.show()
        #time.sleep(.5)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        print("Initialized NeoPixels")
        
    def resetMode(self):
        self.currentLightMode = "NONE"
        
    def activateMotionAlarmMode(self):
        self.currentLightMode = "MOTION_ALARM"
        
    def activateWindowAlarmMode(self):
        self.currentLightMode = "WINDOW_ALARM"
        
    def activateCustomLightMode(self):
        self.currentLightMode = "CUSTOM_LIGHTS"
        
    def setCustomNeopixelColors(self, red, green, blue):
        self.customRed = red
        self.customGreen = green
        self.customBlue = blue
        
    #Main Class Thread
    def runNeoPixelInteface(self):
        while not self.terminate:
            #print(self.currentLightMode)
            if(self.currentLightMode == "NONE"):
                self.pixels.fill((0, 0, 0))
            elif(self.currentLightMode == "MOTION_ALARM"):
                self.exeMotionAlarm()
            elif(self.currentLightMode == "WINDOW_ALARM"):
                self.exeWindowAlarm()
            elif(self.currentLightMode == "CUSTOM_LIGHTS"):
                self.exeCustomLights()
            time.sleep(.1) #Sleep to slow down cpu usage when NONE
        print("NeoPixels Shutdown Complete")
           
    def exeMotionAlarm(self):
        #Set to RED
        for i in range(0,10):
            self.pixels.fill((255, 0, 0))
            time.sleep(.2)
            self.pixels.fill((0, 0, 0))
            time.sleep(.2)
    
    def exeWindowAlarm(self):
        #Set to BLUE
        for i in range(0,10):
            self.pixels.fill((0, 0, 255))
            time.sleep(.2)
            self.pixels.fill((0, 0, 0))
            time.sleep(.2)
    
    def exeCustomLights(self):
        self.pixels.fill((self.customRed, self.customGreen, self.customBlue))
        
    def randomTest(self):
        while(not self.terminate):
            for i in range(0, 12):
                rand1 = random.randint(0,255)
                rand2 = random.randint(0,255)
                rand3 = random.randint(0,255)
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (rand1, rand2, rand3)
                time.sleep(.5)
            for i in range(0, 12):
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (0, 0, 0)
                time.sleep(.5)    
        
    def shutdown(self):
        self.terminate = True
        self.pixels.fill((0, 0, 0))