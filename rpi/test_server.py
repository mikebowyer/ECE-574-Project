import socket
import sys, select
from src.security_message import SecurityMessage
import src.security_message

def server_program():
    # get the hostname
    # host = socket.gethostname()
    host = "192.168.1.8"
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

        data = input('What would you like to do? r=recieve, s=send current system state, t=trigger alarm, c=change, e=exit, reset=reset\n')
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
        elif "t" in data:
            if "1" in data:
                print("Simulating alarm triggered by motion detected event!:\n")       
                security_sys_state.set_alarm_triggered(True, "motion")
                security_sys_state.set_lights_color(0,255,0)
            if "2" in data:
                print("Simulating alarm triggered by door/window opened event!:\n")       
                security_sys_state.set_alarm_triggered(True, "window")
                security_sys_state.set_lights_color(0,0,255)
        elif "reset" in data:
            security_sys_state.reset_everything()
        else:
            pass
            
    conn.close()  # close the connection
    


if __name__ == '__main__':

    for n in range(0,100):
        server_program()