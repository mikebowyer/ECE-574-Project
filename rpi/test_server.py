import socket
import sys, select
from src.security_message import SecurityMessage
import src.security_message

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
    server_socket.listen(2)

    # Create initial state of security system
    security_sys_state = SecurityMessage()
    
    # Wait for connections from clients
    print("Waiting for connections...\n")
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    conn.settimeout(1) # set recv wait time

    # Send starting state
    print("Sending initial state.\n")
    string_to_send = security_sys_state.assemble_packet_to_send()
    bytestream = bytes(string_to_send, 'utf-8')
    while True:

        data = input('What would you like to do? r=recieve, s=send, c=change, e=exit, reset=reset\n')
        if "e" in data:
            exit
        elif "r" in data:
            print("Recieving latest data from app:\n")
            try:
                recieved_str = ""
                next_byte = ""
                next_byte_decoded = ""
                while next_byte_decoded != "\n":
                    next_byte = conn.recv(1)
                    next_byte_decoded = next_byte.decode()
                    recieved_str += next_byte_decoded
                    # print(next_byte_decoded)
                print(recieved_str)
            except: 
                pass
        elif "s" in data:
            print("Sending current system state to app:\n")         
            string_to_send = security_sys_state.assemble_packet_to_send()
            bytestream = bytes(string_to_send, 'utf-8')
            conn.send(bytestream)
        elif "c" in data:
            print("Changing Alaram and light state!:\n")       
            # security_sys_state.set_alarm_state(True)
            # security_sys_state.set_light_state(True)
            security_sys_state.set_lights_on_time(1,1)
            security_sys_state.set_lights_off_time(2,2)
            # security_sys_state.set_selected_audio_clip(2)
            security_sys_state.set_alarm_triggered(True, "motion")
        elif "reset" in data:
            security_sys_state.reset_everything()
        else:
            pass
            
    conn.close()  # close the connection
    


if __name__ == '__main__':

    for n in range(0,100):
        server_program()