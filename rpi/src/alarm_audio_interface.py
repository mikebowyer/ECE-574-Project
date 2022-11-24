from pydub import AudioSegment
from pydub.playback import play

class AlarmAudioInterface:
        
    def init(self):
        print("Initialize Alarm Audio")
        
    def playAlertSound(self):
        print("[INFO] Playing Alert Sound")
        audio = AudioSegment.from_mp3("resources/MetalGearSolidAlert.mp3")
        play(audio)

    def playAlarmSound(self):
        print("[INFO] Playing Alarm Sound")
        audio = AudioSegment.from_mp3("resources/DangerAlarm.mp3")
        play(audio)
