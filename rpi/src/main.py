import time
import threading
import tcp_interface

import neopixel_interface
import motion_sensor_interface
import window_sensor_interface
import alarm_audio_interface
import data_repository

DATA_REPO = data_repository.DataRepository()

SERVER_ADDR = "192.168.1.8"
SERVER_PORT = 5000

RESET = False
TERMINATE = False

def runUserInterface():
    global TERMINATE
    global RESET
    while(not TERMINATE):
        userInput = input("""
/////////////////////////////
Enter:
r) reset system
q) quit
////////////////////////////\n""")
        if(userInput == "r"):
            RESET = True
        elif(userInput == "q"):
            TERMINATE = True
        else:
            print("[ERROR] Invalid input in userInput")
        
def main():
    global DATA_REPO
    global RESET
    
    #Testing Configuration
    #NOTE 1: NeoPixels needs to run as root
    #NOTE 2: AlarmAudio (Pydub) causes issues when run as root (currently...need to fix this)
    useUserInterface = True
    useSockets = False
    useNeoPixels = False
    useMotionSensor = False
    useWindowSensor = False
    useAlarmAudio = False
    
    #NeoPixel Interface
    neopixelInterface = None
    neopixelThread = None
    
    #Window/Door Sensor Interface
    windowSensorInterface = None
    windowSensorThread = None
    
    #TCP Interface
    tcpInterface = None
    tcpThread = None
    
    #Alarm Audio Interface
    alarmAudioInterface = None
    alarmAudioThread = None
    
    
    if(useNeoPixels):
        neopixelInterface = neopixel_interface.NeopixelInterface()
        neopixelInterface.init()
        neopixelThread = threading.Thread(target=neopixelInterface.runNeoPixelInteface, args=())
        neopixelThread.start()
        
    if(useMotionSensor):
        motionSensorInterface = motion_sensor_interface.MotionSensorInterface()
        motionSensorInterface.init()
        motionSensorThread = threading.Thread(target=motionSensorInterface.runSensorInterface, args=())
        motionSensorThread.start()
    
    if(useWindowSensor):
        windowSensorInterface = window_sensor_interface.WindowSensorInterface()
        windowSensorInterface.init()
        windowSensorThread = threading.Thread(target=windowSensorInterface.runSensorInterface, args=())
        windowSensorThread.start()

    if(useUserInterface):
        userInterfaceThread = threading.Thread(target=runUserInterface, args=())
        userInterfaceThread.start()
    
    if(useSockets):
        global RX_ADDR
        global RX_PORT        
        tcpInterface = tcp_interface.TCPInterface()
        tcpInterface.init(SERVER_ADDR, SERVER_PORT)
        tcpThread = threading.Thread(target=tcpInterface.server_program, args=())
        tcpThread.start()
        
    if(useAlarmAudio):
        alarmAudioInterface = alarm_audio_interface.AlarmAudioInterface()
        alarmAudioThread = threading.Thread(target=alarmAudioInterface.runAlarmAudioInteface, args=())
        alarmAudioThread.start()

    ########################################
    #Do magical processing
    ########################################
    alarmTripped = False
    prevAlarmTripped = False
    
    prevAlarmReadyForReset = True
    while not TERMINATE:
        alarmReadyForReset = True #reset ready unless proven otherwise
        
        if(RESET):
            alarmTripped = False
            RESET = False
            alarmAudioInterface.resetMode()
        
        if(useMotionSensor):
            #print(str(motionSensorInterface.alarmTripped()))
            alarmTripped = alarmTripped or motionSensorInterface.alarmTripped()
            #alarmReadyForReset = alarmReadyForReset and (not motionSensorInterface.alarmTripped())
            if(useAlarmAudio and alarmTripped()):
                alarmAudioInterface.activateAlertSound()
                
            if(useNeoPixels and alarmTripped()):
                neopixelInterface.activateWindowAlarmMode()
                
        if(useWindowSensor):
            #p rint("SENSOR VALUE: " + str(windowSensorInterface.alarmTripped()))
            alarmTripped = alarmTripped or windowSensorInterface.alarmTripped()
            alarmReadyForReset = alarmReadyForReset and (not windowSensorInterface.alarmTripped())
            
            if(useAlarmAudio and alarmTripped):
                alarmAudioInterface.activateAlarmSound()
                
            if(useNeoPixels and alarmTripped):
                neopixelInterface.activateWindowAlarmMode()
        
        if(alarmTripped):
            if(prevAlarmTripped == False):
                print("[WARNING] ALARM TRIPPED\n")      
        else:
            if(prevAlarmTripped == True):
                print("[INFO] ALARM RESET\n")
                if(useNeoPixels):
                    neopixelInterface.resetMode()
                    
        
        if(prevAlarmTripped):
            if(alarmReadyForReset and prevAlarmReadyForReset == False):
                    print("[INFO] ALARM READY TO RE-ARM\n")
            
        prevAlarmTripped = alarmTripped
        prevAlarmReadyForReset = alarmReadyForReset
        
        time.sleep(.1) #check at 10 Hz to lower CPU usage
                  
    print("Exiting Main Loop")
    
    #Quit first based on console input
    if(useUserInterface):
        userInterfaceThread.join()

    #Thread Cleanup
    if(useSockets):
        tcpInterface.shutdown()
        tcpThread.join()
        
    #NeoPixel cleanup   
    if(useNeoPixels):
        neopixelInterface.shutdown()
        
    if(useWindowSensor):
        windowSensorInterface.shutdown()
        windowSensorThread.join()
        
    if(useMotionSensor):
        motionSensorInterface.shutdown()
        motionSensorThread.join()
        
    if(useAlarmAudio):
        alarmAudioInterface.shutdown()
        alarmAudioThread.join()
        
        
    print("Exiting")
  
if __name__=="__main__":
    main()
