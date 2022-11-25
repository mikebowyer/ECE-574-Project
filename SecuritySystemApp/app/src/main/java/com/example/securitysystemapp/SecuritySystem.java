package com.example.securitysystemapp;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class SecuritySystem {
    public int mes_len = 26; // Number of characters in message string
    public int control_byte = -1;
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
    public Context service_context;

    public SecuritySystem(Context serviceContext)
    {
        service_context = serviceContext;
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
            int alarm_byte = getByteFromHexChars(message.charAt(2), message.charAt(3));
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
        if (enable_lights_on_off == true)
        {
            int lights_byte = getByteFromHexChars(message.charAt(4), message.charAt(5));
            if (lights_byte == 255)
            {
                lights = 1;
            }
            else
            {
                lights =0;
            }
        }
        boolean enable_light_on_time = isBitAtPositionSet(enable_byte, 2);
        if (enable_light_on_time == true)
        {
            light_on_min = getByteFromHexChars(message.charAt(6), message.charAt(7));
            light_on_hour = getByteFromHexChars(message.charAt(8), message.charAt(9));
        }

        boolean enable_light_off_time = isBitAtPositionSet(enable_byte, 3);
        if (enable_light_off_time == true)
        {
            light_off_min = getByteFromHexChars(message.charAt(10), message.charAt(11));
            light_off_hour = getByteFromHexChars(message.charAt(12), message.charAt(13));
        }
        boolean enable_light_colors = isBitAtPositionSet(enable_byte, 4);
        boolean enable_alarm_audio_clip = isBitAtPositionSet(enable_byte, 5);
        if (enable_alarm_audio_clip == true)
        {
            selected_audio_clip = getByteFromHexChars(message.charAt(20), message.charAt(21));
        }
        boolean enable_alarm_triggered = isBitAtPositionSet(enable_byte, 6);
        if (enable_alarm_triggered == true)
        {
            int alarm_triggered_byte = getByteFromHexChars(message.charAt(22), message.charAt(23));
            if (alarm_triggered_byte == 255)
            {
                alarm_triggered = 1;
                alarm_trigger_event = getByteFromHexChars(message.charAt(24), message.charAt(25));
                NotificationCompat.Builder builder = new NotificationCompat.Builder(service_context, "ALARM")
                        .setSmallIcon(R.drawable.ic_launcher_foreground)
                        .setContentTitle("HI")
                        .setContentText("mom!")
                        .setPriority(NotificationCompat.PRIORITY_DEFAULT);
                NotificationManagerCompat notificationManager = NotificationManagerCompat.from(service_context);

// notificationId is a unique int for each notification that you must define
                notificationManager.notify(1, builder.build());
            }
            else
            {
                alarm_triggered =0;
            }
        }
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


    public String getDataToSend() {
        control_byte = 0;
        String returnString = getAlarmStateHexString();
        returnString += getLightStateHexString();
        returnString += getLightsOnTimeHexString();
        returnString += getLightsOffTimeHexString();
        returnString += "00"; // Lights Color: Blue
        returnString += "00"; // Lights Color: green
        returnString += "00"; // Lights Color: red
        returnString += getSelectedAudioClipHexString(); // Alarm audio clip
        returnString += "00"; // Alarm triggered
        returnString += "00"; // Alarm event
        return getControlHexSendString() + returnString;
    }

    private String getControlHexSendString()
    {
        return String.format("%02X", (0xFF & control_byte));

    }
    private String getAlarmStateHexString()
    {
        if(alarm_armed == 1)
        {
            control_byte = control_byte | 0x1;
            return "FF";
        }
        else
        {
            if (alarm_armed == 0)
            {
                control_byte = control_byte | 0x1;
            }
            return "00";
        }
    }
    private String getLightStateHexString()
    {
        if(lights == 1)
        {
            control_byte = control_byte | 0x2;
            return "FF";
        }
        else
        {
            if (lights == 0)
            {
                control_byte = control_byte | 0x2;
            }
            return "00";
        }
    }
    private String getLightsOnTimeHexString()
    {
        if(light_on_min != -1 && light_on_hour != -1)
        {
            control_byte = control_byte | 0x4;
            String min_hex = String.format("%02X", (0xFF & light_on_min));
            String hour_hex = String.format("%02X", (0xFF & light_on_hour));

            return min_hex + hour_hex;
        }
        else
        {
            return "0000";
        }
    }
    private String getLightsOffTimeHexString()
    {
        if(light_off_min != -1 && light_off_hour != -1)
            {
                control_byte = control_byte | 0x8;
                String min_hex = String.format("%02X", (0xFF & light_off_min));
                String hour_hex = String.format("%02X", (0xFF & light_off_hour));

                return min_hex + hour_hex;
            }
            else
            {
                return "0000";
        }
    }

    private String getSelectedAudioClipHexString()
    {
        if(selected_audio_clip != -1)
        {
            control_byte = control_byte | 0x20;
            return String.format("%02X", (0xFF & selected_audio_clip));
        }
        else
        {
            return "00";
        }
    }

}
