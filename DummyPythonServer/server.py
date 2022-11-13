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
    # conn.settimeout(1)
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
        # user_input = input('\nR for recieve, T for Transmit, E for exit: ')
        user_input = "R"
        if  "R" in user_input:
            recieved_str = ""
            next_byte = ""
            next_byte_decoded = ""
            while next_byte_decoded != "\n":
                next_byte = conn.recv(1)
                next_byte_decoded = next_byte.decode()
                recieved_str += next_byte_decoded
                # print(next_byte_decoded)
            print(recieved_str)
            # print("Not Decoded:")
            # print(data.hex())
        elif "T" in user_input:
            conn.send(b"\x00\x00\x00\n")
        elif "E" in user_input:
            break


        # conn.send(data.encode())  # send data to the client
        # PACKET_SIZE = 1024
        # line = "random len of line here"
        # conn.send(b"00\n")
        # data = input(' -> ')


    conn.close()  # close the connection
    


if __name__ == '__main__':

    for n in range(0,100):
        server_program()