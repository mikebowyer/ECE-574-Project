import time

import threading
import tcp_interface

import neopixel_interface
import motion_sensor_interface
import window_sensor_interface
import alarm_audio_interface

ANDROID_ADDR = "192.168.1.8"
ANDROID_PORT = 5000 

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
    global terminate
    
    #NeoPixel Interface
    neopixInterface = None
    pixelThread = None
    
    #Window/Door Sensor Interface
    windowSensorInterface = None
    windowSensorThread = None
    
    #TCP Interface
    tcpInterface = None
    tcpThread = None
    
    #Alarm Audio Interface
    alarmAudioInterface = alarm_audio_interface.AlarmAudioInterface()
    
    #NeoPixel Interface
    neopixInterface = neopixel_interface.NeopixelInterface()
    neopixInterface.init()
     
    #Motion Sensor Interface
    motionSensorInterface = motion_sensor_interface.MotionSensorInterface()
    motionSensorInterface.init()
    motionSensorThread = threading.Thread(target=motionSensorInterface.runSensor, args=())
    motionSensorThread.start()
    
    #Window Sensor
    #windowSensorInterface = window_sensor_interface.WindowSensorInterface()
    #windowSensorInterface.init()
    #windowSensorInterface.test()
    #windowSensorThread = threading.Thread(target=windowSensorInterface.runSensor, args=())
    #windowSensorThread.start()
    
    #Door Sensor
    #TODO

    #User Interface 
    userInterfaceThread = threading.Thread(target=user_interface_read, args=())
    userInterfaceThread.start()
    
    #TCP Interface
    global RX_ADDR
    global RX_PORT        
    #tcpInterface = tcp_interface.TCPInterface()
    #tcpInterface.init(ANDROID_ADDR, ANDROID_PORT)
    #tcpThread = threading.Thread(target=tcpInterface.server_program, args=())
    #tcpThread.start()
        
    ########################################
    #Do magical processing
    ########################################
    while not terminate:
        time.sleep(.1) #check at 10 Hz
        print(str(motionSensorInterface.alarmTripped()))
        if((motionSensorInterface.alarmTripped() == True)):
        #if((motionSensorInterface.alarmTripped() == True) or
        #   (windowSensorInterface.alarmTripped() == True)):
            #alarmAudioInterface.playAlertSound()
            neopixInterface.motionAlarm()
    print("Exiting Main Loop")
    
    ########################################
    #Thread Cleanup
    ########################################
    
    #Quit first based on console input
    userInterfaceThread.join()
        
    #NeoPixel Cleanup   
    neopixInterface.shutdown()
     
    #Window Sensor Cleanup
    #windowSensorInterface.shutdown()
    #windowSensorThread.join()
    
    #Motion Sensor Cleanup
    motionSensorInterface.shutdown()
    motionSensorThread.join()
    
    #TCP Cleanup
    #tcpInterface.shutdown()
    #tcpThread.join()    
        
    print("Exiting")
  
if __name__=="__main__":
    main()

