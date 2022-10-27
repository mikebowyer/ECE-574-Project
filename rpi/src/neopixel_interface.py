import board
import neopixel

import time
import random

class NeopixelInterface:
    pixels = None
    terminate = False
    def init(self):
        self.pixels = neopixel.NeoPixel(board.D18, 12)
        self.pixels.fill((127, 127, 127))
        self.pixels.show()
        time.sleep(.5)
        self.pixels.fill((0, 0, 0))
        print("Initialized NeoPixels")
           
    def motionAlarm(self):
        for i in range(0,10):
            self.pixels.fill((255, 0, 0))
            time.sleep(.2)
            self.pixels.fill((0, 0, 0))
            time.sleep(.2)
    
    def windowAlarm(self):
        for i in range(0,10):
            self.pixels.fill((0, 0, 255))
            time.sleep(.2)
            self.pixels.fill((0, 0, 0))
            time.sleep(.2)
        
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
        
    def runPixels(self):
        #self.randomTest()
        #self.motionAlarm()
        self.windowAlarm()
        pass
        
    def shutdown(self):
        self.terminate = True
        self.pixels.fill((0, 0, 0))
        print("NeoPixels Shutdown Complete")