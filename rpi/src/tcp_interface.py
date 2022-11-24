import socket
import sys, select
import security_message

class TCPInterface:
    # get the hostname
    # host = socket.gethostname()
    #host = "192.168.0.109"
    #port = 5000  # initiate port no above 1024
    server_socket = None
    security_sys_state = None
    terminate = False
    conn = None
    address = None
    
    def init(self, rpiAddr, rpiPort):
        print("Hostname and Port: " + str(rpiAddr) +":" + str(rpiPort))

        self.server_socket = socket.socket()  # get instance
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((rpiAddr, rpiPort))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)

        # Create initial state of security system
        self.security_sys_state = security_message.SecurityMessage()
        
    def server_program(self):
        
        # Wait for connections from clients
        print("Waiting for connections...\n")
        self.conn, self.address = self.server_socket.accept()  # accept new connection
        print("Connection from: " + str(self.address))
        self.conn.settimeout(1) # set recv wait time
        
        received_str = ""
        # Send starting state
        print("Sending initial state.\n")
        while not self.terminate:
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
                    next_byte = self.conn.recv(1)
                    next_byte_decoded = next_byte.decode()
                    recieved_str += next_byte_decoded
                    # print(next_byte_decoded)
            except: 
                pass
            print(recieved_str)
            
            mypacket= security_message.SecurityMessage()
            mypacket.set_alarm_state(True)
            string_to_send = mypacket.assemble_packet_to_send()
            bytestream = bytes(string_to_send, 'utf-8')
            self.conn.send(bytestream)
            
            # conn.send(data.encode())  # send data to the client
            # PACKET_SIZE = 1024
            # line = "random len of line here"
            # conn.send(b"00\n")
            # data = input(' -> ')
            
        self.conn.close()  # close the connection
        print("TCP Shutdown Complete")
        
    def shutdown(self):
        self.terminate = True
