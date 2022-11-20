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

    def reset_everything(self):
        self.control = 0x00
        self.alarm_state = 0x00
        self.lights = 0x00
        self.light_on_hour = 0x00
        self.light_on_min = 0x00
        self.light_off_hour = 0x00
        self.light_off_min = 0x00
        self.lights_color_red = 0x00
        self.lights_color_green = 0x00
        self.lights_color_blue = 0x00
        self.selected_audio_clip = 0x00
        self.alarm_triggered = 0x00
        self.alarm_trigger_event = 0x00

    def assemble_packet_to_send(self):
        string_to_send = ""
        string_to_send+=f'{self.control:02x}' # Left Most
        string_to_send+=f'{self.alarm_state:02x}'
        string_to_send+=f'{self.lights:02x}'
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
        self.control = self.control | 0x01
        if state:
            self.alarm_state = 0xFF
        else:
            self.alarm_state = 0x00

    def set_light_state(self, state):
        self.control = self.control | 0x02
        if state:
            self.light_state = 0xFF
        else:
            self.light_state = 0x00
