import time
import threading
import tcp_interface

import neopixel_interface
import motion_sensor_interface
import window_sensor_interface
import alarm_audio_interface
import security_message

DATA_REPO = security_message.SecurityMessage()

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
    prevAlarmOn = False
    prevLightOn = False
    
    alarmTypeDict = {"WINDOW1" : False, "DOOR1" : False, "MS1" : False}
        
    #Testing Configuration
    #NOTE 1: NeoPixels needs to run as root
    #NOTE 2: AlarmAudio (Pydub) causes issues when run as root (currently...need to fix this)
    useUserInterface = True
    useSockets = True
    useNeoPixels = True
    useMotionSensor = True
    useWindowSensor = True
    useAlarmAudio = True
    
    print("Initial Conditions:")
    print("Alarm On: " + str(DATA_REPO.get_alarm_state()))
    print("Lights On: " + str(DATA_REPO.get_light_state()))
    print("Lights On Time Hour: " + str(DATA_REPO.get_lights_on_time_hour_min_tuple()[0]))
    print("Lights On Time Min: " + str(DATA_REPO.get_lights_on_time_hour_min_tuple()[1]))
    print("Lights Off Time Hour: " + str(DATA_REPO.get_lights_off_time_hour_min_tuple()[0]))
    print("Lights Off Time Min: " + str(DATA_REPO.get_lights_off_time_hour_min_tuple()[1]))
    print("Blue Color: " + str(DATA_REPO.get_lights_color_blue()))
    print("Green Color: " + str(DATA_REPO.get_lights_color_green()))
    print("Red Color: " + str(DATA_REPO.get_lights_color_red()))
    print("Audio Clip Num: " + str(DATA_REPO.get_selected_audio_clip()))

    
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
        tcpInterface.set_current_system_state(DATA_REPO) #send app all current values
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
        #Receive Commands from App
        if(useSockets):
            DATA_REPO = tcpInterface.get_current_system_state()
        
###############
#Process Lights
###############
        if(useNeoPixels):
            
            if(alarmTypeDict["MS1"] == True):
                neopixelInterface.activateMotionAlarmMode()
            elif(alarmTypeDict["WINDOW1"] == True):
                neopixelInterface.activateWindowAlarmMode()
              
            if((DATA_REPO.get_light_state() == True) and (alarmTripped == False)):
                if(prevLightOn == False):
                    print("[INFO] Lights Turned On")
                if(DATA_REPO.get_alarm_triggered() == False):
                    #100 works
                    neopixelInterface.setCustomNeopixelColors(100, 100, 100)
                    
                    #draws too much power
                    #neopixelInterface.setCustomNeopixelColors(128, 128, 128)
                    
                    #draws too much power
                    #neopixelInterface.setCustomNeopixelColors(255, 255, 255)
                    neopixelInterface.activateCustomLightMode()
            elif(alarmTripped == False):
                if(prevLightOn == True):
                    print("INFO] Lights Turned Off")
                    neopixelInterface.resetMode()
            prevLightOn = DATA_REPO.get_light_state()
            
###############
#Process Audio
###############            
        if(useAlarmAudio):
            if(alarmTypeDict["WINDOW1"] == True):
                alarmAudioInterface.activateAlarmSound()
                
            elif(alarmTypeDict["MS1"] == True):
                alarmAudioInterface.activateAlertSound()

########################################
## PROCESS MAIN ALARM LOGIC
########################################
        #print(alarmTripped)
        if(DATA_REPO.get_alarm_state()):
            if(prevAlarmOn == False):
                print("[INFO] Alarm Turned On")
            alarmReadyForReset = True #reset ready unless proven otherwise  
            if(RESET):
                print("[INFO] RESETING ALARM")
                alarmTripped = False
                RESET = False
                alarmTypeDict["WINDOW1"] = False
                alarmTypeDict["MS1"] = False
                
                if(useNeoPixels):
                    print("RESET NEOs")
                    neopixelInterface.resetMode()
                
                if(useAlarmAudio):
                    alarmAudioInterface.resetMode()
            
            if(useMotionSensor):
                #print(str(motionSensorInterface.alarmTripped()))
                if((DATA_REPO.get_alarm_state() == True) and motionSensorInterface.alarmTripped()):
                    alarmTypeDict["MS1"] = True
                
                alarmTripped = alarmTripped or motionSensorInterface.alarmTripped()
                alarmReadyForReset = alarmReadyForReset and (not motionSensorInterface.alarmTripped())            
         
            if(useWindowSensor):
                #print("SENSOR VALUE: " + str(windowSensorInterface.alarmTripped()))
                if((DATA_REPO.get_alarm_state() == True) and windowSensorInterface.alarmTripped()):
                    alarmTypeDict["WINDOW1"] = True
                
                alarmTripped = alarmTripped or windowSensorInterface.alarmTripped()
                alarmReadyForReset = alarmReadyForReset and (not windowSensorInterface.alarmTripped())
            
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
        
        else: #if alarm not turned on
            if(prevAlarmOn == True):
                print("[INFO] Alarm Turned Off")
        #Write Updates to App
        if(useSockets):
            #DATA_REPO.set_alarm_state(False)
            triggerEvent = "unknown"
            if(alarmTypeDict["WINDOW1"] == True):
                triggerEvent = "window"
            elif(alarmTypeDict["MS1"] == True):
                triggerEvent = "motion"           
            DATA_REPO.set_alarm_triggered(alarmTripped, triggerEvent)
            tcpInterface.set_current_system_state(DATA_REPO)
        
        #Set All current Values as previous 
        prevAlarmOn = DATA_REPO.get_alarm_state()
        prevLightOn = DATA_REPO.get_light_state()
        time.sleep(.1) #check at 10 Hz to lower CPU usage

########################################
##CLEANUP
########################################
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
        
    print("Exiting Program")
  
if __name__=="__main__":
    main()

