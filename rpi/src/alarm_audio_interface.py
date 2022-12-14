import time
import os
from pydub import AudioSegment
from pydub.playback import play

class AlarmAudioInterface:
    terminate = False
    currentAudioMode = "NONE"
    activated = False
    prevActivated = False
        
    def init(self):
        print("Initialize Alarm Audio")
        
    def resetMode(self):
        self.currentAudioMode = "NONE"
        self.prevActivated = False
        
    #Main Class Thread
    def runAlarmAudioInteface(self):
        while not self.terminate:
            if(self.currentAudioMode == "NONE"):
                pass
            if(self.currentAudioMode == "ALERT"): #ALERT
                self.playAlertSound()
            elif(self.currentAudioMode == "ALARM"): #SCREAM
                self.playAlarmSound()
            elif(self.currentAudioMode == "SPOOKY"): #SPOOKY
                self.playSpookySound()
            time.sleep(.1) #Sleep to slow down cpu usage when NONE
            
    def activateAlertSound(self):
        if(self.prevActivated == False):
            print("[INFO] Activating Alert Sound")
        self.currentAudioMode = "ALERT"
        self.prevActivated = True
        
    def activateAlarmSound(self):
        if(self.prevActivated == False):
            print("[INFO] Activating Alarm Sound")
        self.currentAudioMode = "ALARM"
        self.prevActivated = True
        
    def activateSpookySound(self):
        if(self.prevActivated == False):
            print("[INFO] Activating Spooky Sound")
        self.currentAudioMode = "SPOOKY"
        self.prevActivated = True
        
    def playAlertSound(self):
        print("[INFO] Playing Alert Sound")
        audio = AudioSegment.from_mp3("resources/MetalGearSolidAlert.mp3")
        play(audio)

    def playAlarmSound(self):
        print("[INFO] Playing Alarm Sound")
        audio = AudioSegment.from_mp3("resources/DangerAlarm.mp3")
        play(audio)
        
    def playSpookySound(self):
        print("[INFO] Playing Spooky Sound")
        audio = AudioSegment.from_mp3("resources/Scarymusic.mp3")
        play(audio)

    def shutdown(self):
        self.terminate = True