import threading
from socket_interface import *

txAddr = "127.0.0.1"
txPort = 5555
rxAddr = "127.0.0.1"
rxPort = 5555
terminate = False

def user_interface_read():
	global terminate
	while(not terminate):
		userInput = input("""
/////////////////////////////
Enter:
q) quit
////////////////////////////\n""")
		if(userInput == "q"):
			terminate = True

def receive():
	global terminate
	while(not terminate):
		temp = 1
		print("TestRx")

def main():
	global rxAddr
	global rxPort
	#Sockets
	rxSock = createRxSocket(rxAddr, rxPort)
	txSock = createTxSocket()
	
	#testPayload = "9999"
	#send(testPayload, txSock, txAddr, txPort)


	#User Input Thread
	userInterfaceThread = threading.Thread(target=user_interface_read, args=())
	userInterfaceThread.start()

	#UDP Receive Thread
	rx_thread = threading.Thread(target=receive, args=())
	rx_thread.start()

	#Thread Cleanup
	rx_thread.join()
	userInterfaceThread.join()
	print("Exiting")
  
if __name__=="__main__":
    main()
