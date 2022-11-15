package com.example.securitysystemapp;

import android.util.Log;

public class SecuritySystem {
    public int expected_message_length = 26; // Number of characters in message string
    public int lights = -1;
    public int light_on_hour = -1;
    public int light_on_min = -1;
    public int light_off_hour = -1;
    public int light_off_min = -1;
    public int lights_color_red = -1;
    public int lights_color_green = -1;
    public int lights_color_blue = -1;
    public int selected_audio_clip = -1;
    public int alarm_triggered = -1;
    public int alarm_trigger_event = -1;
    public SecuritySystem()
    {

    }

    public void setStateWithReceivedPacket(String message)
    {
        Log.i("SecuritySystem","Parsing input message");
        if( message.length() != expected_message_length)
        {
            Log.e("SecuritySystem","not correct length");
        }
        else
        {
            parseMessageUpdateState(message);
        }
    }

    public void parseMessageUpdateState(String message)
    {
        Character enable_byte_msb = message.charAt(0);
        Character enable_byte_lsb = message.charAt(1);
        int enable_byte_msb_int = enable_byte_msb.digit(enable_byte_msb,16);
        String binaryString = Integer.toBinaryString(enable_byte_msb_int);
        byte bitMask = (byte)(0x8<<(byte)enable_byte_msb_int);
        Log.i("Test","feck");



    }
}
