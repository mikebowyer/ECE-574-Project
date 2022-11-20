import socket
import sys, select

def server_program():
    # get the hostname
    # host = socket.gethostname()
    host = "192.168.0.109"
    port = 5000  # initiate port no above 1024
    print("Hostname and Port: " + str(host) +":" + str(port))

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    print("Waiting for connections...\n")
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    conn.settimeout(1)
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        # data = conn.recv(1024).decode()
        # data = conn.recv(1).decode()
        # print("Data:")
        # print(data)
        # if not data:
        #     # if data is not received break
        #     break
        # print("from connected user: " + str(data))
        
        # Recieve 
        try:
            recieved_str = ""
            next_byte = ""
            next_byte_decoded = ""
            while next_byte_decoded != "\n":
                next_byte = conn.recv(1)
                next_byte_decoded = next_byte.decode()
                recieved_str += next_byte_decoded
                # print(next_byte_decoded)
        except: 
            pass
        print(recieved_str)
        

        mypacket= Packet()
        mypacket.set_alarm_state(True)
        string_to_send = mypacket.assemble_packet_to_send()
        bytestream = bytes(string_to_send, 'utf-8')
        conn.send(bytestream)

        # conn.send(data.encode())  # send data to the client
        # PACKET_SIZE = 1024
        # line = "random len of line here"
        # conn.send(b"00\n")
        # data = input(' -> ')


    conn.close()  # close the connection
    
class Packet:
    enable = 0x00
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
        self.enable = 0x00
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
        string_to_send+=f'{self.enable:02x}'
        string_to_send+=f'{self.alarm_trigger_event:02x}'
        string_to_send+=f'{self.alarm_triggered:02x}'
        string_to_send+=f'{self.selected_audio_clip:02x}'
        string_to_send+=f'{self.lights_color_blue:02x}'
        string_to_send+=f'{self.lights_color_green:02x}'
        string_to_send+=f'{self.lights_color_red:02x}'
        string_to_send+=f'{self.light_off_min:02x}'
        string_to_send+=f'{self.light_off_hour:02x}'
        string_to_send+=f'{self.light_on_min:02x}'
        string_to_send+=f'{self.light_on_hour:02x}'
        string_to_send+=f'{self.lights:02x}'
        string_to_send+=f'{self.alarm_state:02x}'
        string_to_send += "\n"

        return string_to_send

    def set_alarm_state(self, state):
        self.enable = self.enable | 0x01
        if state:
            self.alarm_state = 0xFF
        else:
            self.alarm_state = 0x00



if __name__ == '__main__':

    for n in range(0,100):
        server_program()