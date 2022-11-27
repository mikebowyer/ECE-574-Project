class SecurityMessage:
    control = 0x00
    alarm_state = 0x00
    lights = 0x00
    light_on_hour = 0x00
    light_on_min = 0x00
    light_off_hour = 0x00
    light_off_min = 0x00
    lights_color_red = 0x00
    lights_color_green = 0x00
    lights_color_blue = 0x00
    selected_audio_clip = 0x00
    alarm_triggered = 0x00
    alarm_trigger_event = 0x00

    def __init__(self):
        self.reset_everything()
        # self.set_alarm_state(False)
        # self.set_light_state(False)
        # self.set_lights_on_time(13,20)
        # self.set_lights_off_time(2,47)
        # self.set_selected_audio_clip(3)
        self.set_alarm_triggered(False)

    def reset_everything(self):
        self.control = 0x00
        self.alarm_state = 0x00
        self.light_state = 0x00
        self.light_on_hour = 0x00
        self.light_on_min = 0x00
        self.light_off_hour = 0x00
        self.light_off_min = 0x00
        self.lights_color_blue = 0x00
        self.lights_color_green = 0x00
        self.lights_color_red = 0x00
        self.selected_audio_clip = 0x00
        self.alarm_triggered = 0x00
        self.alarm_trigger_event = 0x00

    def assemble_packet_to_send(self):
        #print("TX ALARM STATE: " + f'{self.alarm_state:02x}')
        
        string_to_send = ""
        string_to_send+=f'{self.control:02x}' # Left Most
        string_to_send+=f'{self.alarm_state:02x}'
        string_to_send+=f'{self.light_state:02x}'
        string_to_send+=f'{self.light_on_min:02x}'
        string_to_send+=f'{self.light_on_hour:02x}'
        string_to_send+=f'{self.light_off_min:02x}'
        string_to_send+=f'{self.light_off_hour:02x}'
        string_to_send+=f'{self.lights_color_blue:02x}'
        string_to_send+=f'{self.lights_color_green:02x}'
        string_to_send+=f'{self.lights_color_red:02x}'
        string_to_send+=f'{self.selected_audio_clip:02x}'
        string_to_send+=f'{self.alarm_triggered:02x}'
        string_to_send+=f'{self.alarm_trigger_event:02x}'
        string_to_send += "\n"

        return string_to_send

    def set_alarm_state(self, state):
        #self.control = self.control | 0x01
        if state:
            self.alarm_state = 0xFF
        else:
            self.alarm_state = 0x00

    def set_light_state(self, state):
        #self.control = self.control | 0x02
        if state:
            self.light_state = 0xFF
        else:
            self.light_state = 0x00

    def set_lights_on_time(self, hour, min):
        #self.control = self.control | 0x04
        self.light_on_hour = hour
        self.light_on_min = min
    
    def set_lights_off_time(self, hour, min):
        #self.control = self.control | 0x08
        self.light_off_hour = hour
        self.light_off_min = min
        
    def set_lights_color_blue(self, colorVal):
        self.lights_color_blue = hex(colorVal)
        
    def set_lights_color_green(self, colorVal):
        self.lights_color_green = hex(colorVal)
        
    def set_lights_color_red(self, colorVal):
        self.lights_color_red = hex(colorVal)

    def set_selected_audio_clip(self, clip_num):
        #self.control = self.control | 0x20
        self.selected_audio_clip = clip_num

    def set_alarm_triggered(self, triggered, trigger_event = "unknown"):
        #self.control = self.control | 0x40

        if triggered:
            self.alarm_triggered = 0xFF
        else: 
            self.alarm_triggered = 0x00

        if "window" in trigger_event or "door" in trigger_event:
            self.alarm_trigger_event = 0x01
        elif "motion" in trigger_event:
            self.alarm_trigger_event = 0x02
        else:
            self.alarm_trigger_event = 0x00
            
    ###########################################
    #RECEIVE FUNCTIONS
    ############################################
    def update_alarm_state(self, rx_string):
        self.alarm_state = int(rx_string[2:4], 16)
            
    def update_light_state(self, rx_string):
        self.light_state = int(rx_string[4:6], 16)
            
    def update_lights_on_time(self, rx_string):
        self.light_on_min = int(rx_string[6:8], 16)
        self.light_on_hour = int(rx_string[8:10], 16)
    
    def update_lights_off_time(self, rx_string):
        self.light_off_min = int(rx_string[10:12], 16)
        self.light_off_hour = int(rx_string[12:14], 16)
        
    def update_lights_color_blue(self, rx_string):
        self.lights_color_blue = int(rx_string[14:16], 16)
        
    def update_lights_color_green(self, rx_string):
        self.lights_color_green = int(rx_string[16:18], 16)
        
    def update_lights_color_red(self, rx_string):
        self.lights_color_red = int(rx_string[18:20], 16)      

    def update_selected_audio_clip(self, rx_string):
        self.selected_audio_clip = int(rx_string[20:22], 16)
            
    def disassemble_packet(self, rx_string):
        #print("RX_STRING: " + rx_string)
        self.update_alarm_state(rx_string)
        self.update_light_state(rx_string)
        self.update_lights_on_time(rx_string)
        self.update_lights_off_time(rx_string)
        self.update_lights_color_blue(rx_string)
        self.update_lights_color_green(rx_string)
        self.update_lights_color_red(rx_string)
        self.update_selected_audio_clip(rx_string)