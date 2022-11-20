package com.example.securitysystemapp;

import android.content.Intent;
import android.util.Log;

public class SecuritySystem {
    public int mes_len = 26; // Number of characters in message string
    public int alarm_armed = -1;
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
        if( message.length() != mes_len)
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
        // Extract and assemble enable information
        int enable_byte = getByteFromHexChars(message.charAt(0), message.charAt(1));

        boolean enable_alarm_on_off = isBitAtPositionSet(enable_byte, 0);
        if (enable_alarm_on_off == true)
        {
            int alarm_byte = getByteFromHexChars(message.charAt(mes_len-2), message.charAt(mes_len-1));
            if (alarm_byte == 255)
            {
                alarm_armed = 1;
            }
            else
            {
                alarm_armed =0;
            }
        }

        boolean enable_lights_on_off = isBitAtPositionSet(enable_byte, 1);
        boolean enable_light_on_time = isBitAtPositionSet(enable_byte, 2);
        boolean enable_light_off_time = isBitAtPositionSet(enable_byte, 3);
        boolean enable_light_colors = isBitAtPositionSet(enable_byte, 4);
        boolean enable_alarm_audio_clip = isBitAtPositionSet(enable_byte, 5);
        boolean enable_alarm_triggered = isBitAtPositionSet(enable_byte, 6);
    }
    public int getByteFromHexChars(Character msb, Character lsb)
    {
        int msb_int = msb.digit(msb,16);
        int lsb_int = lsb.digit(lsb,16);
        int bits_to_shift = 4;
        int msb_int_shifted = msb_int << (bits_to_shift);
        return msb_int_shifted | lsb_int;
    }

    public boolean isBitAtPositionSet(int byte_in, int position_of_interest)
    {
        int bit_mask = 1 << (position_of_interest);
        int byte_in_masked = byte_in & bit_mask;
        return byte_in_masked != 0;
    }

    public String getAlarmStateString()
    {
        String returnString = "Alarm Armed: ";
        if (alarm_armed == 1)
        {
            returnString += "On";
        }
        else if (alarm_armed == 0)
        {
            returnString += "Off";
        }
        else
        {
            returnString += "Unknown";
        }
        return returnString;

    }
}
