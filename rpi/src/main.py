import threading
from socket_interface import *

import neopixel_interface
import motion_sensor_interface
import window_sensor_interface
import alarm_audio_interface

TX_ADDR = "192.168.1.12"
TX_PORT = 5555
RX_ADDR = "127.0.0.1"
RX_PORT = 5555
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

def receive(rxSocket):
    global terminate
    while(not terminate):
        print("TestRx")
           
def transmit(txSocket):
    global terminate
    global TX_ADDR
    global TX_PORT
    message_data = b"TESTING"
    while(not terminate):
        print("Sending")
        send(message_data, txSocket, TX_ADDR, TX_PORT)
        
def main():
    
    #Testing Configuration
    useUserInterface = True
    useSockets = False
    useNeoPixels = False
    useMotionSensor = False
    useWindowSensor = True
    useAlarmAudio = False
    
    #NeoPixel Interface
    neopixInterface = None
    pixelThread = None
    
    #Window/Door Sensor Interface
    windowSensorInterface = None
    windowSensorThread = None
    
    
    if(useNeoPixels):
        neopixInterface = neopixel_interface.NeopixelInterface()
        neopixInterface.init()
        pixelThread = threading.Thread(target=neopixInterface.runPixels, args=())
        pixelThread.start()
        
    if(useMotionSensor):
        motionSensorInterface = motion_sensor_interface.MotionSensorInterface()
        motionSensorInterface.init()
    
    if(useWindowSensor):
        windowSensorInterface = window_sensor_interface.WindowSensorInterface()
        windowSensorInterface.init()
        windowSensorInterface.test()
        windowSensorThread = threading.Thread(target=windowSensorInterface.runSensor, args=())
        windowSensorThread.start()

    if(useUserInterface):
        userInterfaceThread = threading.Thread(target=user_interface_read, args=())
        userInterfaceThread.start()
    
    if(useSockets):
        global RX_ADDR
        global RX_PORT
        rxSock = createRxSocket(RX_ADDR, RX_PORT)
        txSock = createTxSocket()
    
        #UDP Receive Thread
        rx_thread = threading.Thread(target=receive, args=(rxSock,))
        rx_thread.start()
    
        #UDP Transmit Thread
        tx_thread = threading.Thread(target=transmit, args=(txSock,))
        tx_thread.start()
        
    if(useAlarmAudio):
        alarmAudioInterface = alarm_audio_interface.AlarmAudioInterface()
        alarmAudioInterface.playAlertSound()
        alarmAudioInterface.playAlarmSound()

    ########################################
    #Do magical processing
    ########################################
    

    #Quit first based on console input
    if(useUserInterface):
        userInterfaceThread.join()

    #Thread Cleanup
    if(useSockets):
        rx_thread.join()
        tx_thread.join()
        
    #NeoPixel cleanup   
    if(useNeoPixels):
        neopixInterface.shutdown()
        pixelThread.join()
        
    if(useWindowSensor):
        windowSensorInterface.shutdown()
        windowSensorThread.join()
        
    print("Exiting")
  
if __name__=="__main__":
    main()

