import time
import threading
import tcp_interface

import neopixel_interface
import motion_sensor_interface
import window_sensor_interface
import alarm_audio_interface

SERVER_ADDR = "192.168.1.8"
SERVER_PORT = 5000

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
        
def main():
    
    #Testing Configuration
    useUserInterface = True
    useSockets = True
    useNeoPixels = True
    useMotionSensor = False
    useWindowSensor = True
    useAlarmAudio = False #Not working
    
    #NeoPixel Interface
    neopixInterface = None
    pixelThread = None
    
    #Window/Door Sensor Interface
    windowSensorInterface = None
    windowSensorThread = None
    
    #TCP Interface
    tcpInterface = None
    tcpThread = None
    
    if(useNeoPixels):
        neopixInterface = neopixel_interface.NeopixelInterface()
        neopixInterface.init()
        
    if(useMotionSensor):
        motionSensorInterface = motion_sensor_interface.MotionSensorInterface()
        motionSensorInterface.init()
        motionSensorInterface.test()
        motionSensorThread = threading.Thread(target=motionSensorInterface.runSensor, args=())
        motionSensorThread.start()
    
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
        tcpInterface = tcp_interface.TCPInterface()
        tcpInterface.init(SERVER_ADDR, SERVER_PORT)
        tcpThread = threading.Thread(target=tcpInterface.server_program, args=())
        tcpThread.start()
        
    if(useAlarmAudio):
        alarmAudioInterface = alarm_audio_interface.AlarmAudioInterface()

    ########################################
    #Do magical processing
    ########################################
    while not terminate:
        time.sleep(.1) #check at 10 Hz
        alarmTripped = False
        if(useMotionSensor):
            #print(str(motionSensorInterface.alarmTripped()))
            alarmTripped = alarmTripped or motionSensorInterface.alarmTripped()
        if(useWindowSensor):
            #print(str(windowSensorInterface.alarmTripped()))
            alarmTripped = alarmTripped or windowSensorInterface.alarmTripped()

        if(alarmTripped):
            if(useNeoPixels):
                neopixInterface.motionAlarm()
            if(useAlarmAudio):
                alarmAudioInterface.playAlertSound()
                pass
                  
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
        neopixInterface.shutdown()
        
    if(useWindowSensor):
        windowSensorInterface.shutdown()
        windowSensorThread.join()
        
    if(useMotionSensor):
        motionSensorInterface.shutdown()
        motionSensorThread.join()
        
    print("Exiting")
  
if __name__=="__main__":
    main()

