class DataRepository:
    alarmStatus = False
    lightsOn = False
    lightsTimerStart = 0 #ms Time since Epoch
    lightsTimerStop = 0 #ms Time since Epoch
    lightsColorBlue = 0 #0-255
    lightsColorGreen = 0 #0-255
    lightsColorRed = 0 #0-255
    selectedAudio = 0 #0=None, 1=Alert, 2=Alarm, 3=...
    alarmTriggered = 0
    alarmTriggeredType = 0 #Door, Window, Motion, etc
    
    def __init__(self):
        self.alarm_state = False
        self.light_state = False
        self.lightsTimerStart = 0
        self.lightsTimerStop = 0
        self.lights_color_blue = 255
        self.lights_color_green = 255
        self.lights_color_red = 255
        self.selected_audio_clip = 0
        self.alarm_triggered = False
        self.alarm_trigger_event = 0     