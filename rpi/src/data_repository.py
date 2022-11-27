class DataRepository:
    alarmStatus = 0
    lightsOn = False
    lightsTimerStart = 0 #ms Time since Epoch
    lightsTimerStop = 0 #ms Time since Epoch
    lightsColorRed = 0 #0-255
    lightsColorGreen = 0 #0-255
    lightsColorBlue = 0 #0-255
    selectedAudio = 0 #0=None, 1=Alert, 2=Alarm, 3=...
    alarmTriggered = 0
    alarmTriggeredType = 0 #Door, Window, Motion, etc
    
    def __init__(self):
        pass
        #self.control = 0x00
        #self.alarm_state = 0x00
        #self.light_state = 0x00
        #self.light_on_hour = 0x00
        #self.light_on_min = 0x00
        #self.light_off_hour = 0x00
        #self.light_off_min = 0x00
        #self.lights_color_red = 0x00
        #self.lights_color_green = 0x00
        #self.lights_color_blue = 0x00
        #self.selected_audio_clip = 0x00
        #self.alarm_triggered = 0x00
        #self.alarm_trigger_event = 0x00
