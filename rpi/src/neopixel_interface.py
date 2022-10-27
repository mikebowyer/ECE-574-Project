import board
import neopixel

import time
import random

class NeopixelInterface:
    pixels = neopixel.NeoPixel(board.D18, 12)
    terminate = False
    def init(self):
        print("Initialize NeoPixels")
        
    def runPixels(self):
        """
        while(not self.terminate):
            for i in range(0, 12):
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (255, 0, 0)
                self.pixels.show()
                time.sleep(.5)
            for i in range(0, 12):
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (0, 0, 0)
                self.pixels.show()
                time.sleep(.5)
        """
        while(not self.terminate):
            for i in range(0, 12):
                rand1 = random.randint(0,255)
                rand2 = random.randint(0,255)
                rand3 = random.randint(0,255)
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (rand1, rand2, rand3)
                self.pixels.show()
                time.sleep(.5)
            for i in range(0, 12):
                #Seems janky
                if(self.terminate):
                    break
                self.pixels[i] = (0, 0, 0)
                self.pixels.show()
                time.sleep(.5)
    
    def testPixel(self):
        self.pixels[0] = (255, 0, 0)
        self.pixels.show()
        
    def shutdown(self):
        self.terminate = True
        for i in range(0,12):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()
        print("NeoPixels Shutdown Complete")