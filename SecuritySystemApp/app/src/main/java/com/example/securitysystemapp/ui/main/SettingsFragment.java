package com.example.securitysystemapp.ui.main;

import android.app.Activity;
import android.app.Dialog;
import android.app.TimePickerDialog;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.securitysystemapp.R;
import com.example.securitysystemapp.SecuritySystem;
import com.example.securitysystemapp.databinding.ControlFragmentBinding;
import com.example.securitysystemapp.databinding.FragmentMainBinding;
import com.example.securitysystemapp.databinding.SettingsFragmentBinding;

/**
 * The fragment for the Settings tab in the main activity.
 */
public class SettingsFragment extends Fragment implements AdapterView.OnItemSelectedListener {
//================================================================================
// class member variables
//================================================================================
    // Background Service information
    TCPService mService;
    boolean mBound = false;

    // UI Elements and context info
    private Context globalContext = null;
    private SettingsFragmentBinding binding;

    // Spinner
    private Spinner spinner;
    private volatile boolean update_from_broadcast = false;

    // On Time Settings
    static final int LIGHTS_ON_TIME_DIALOG_ID = 1111;
    private TextView onTimeView;
    private int onTimeHour = 12;
    private int onTimeMin = 0;

    // Off Time Settings
    static final int LIGHTS_OFF_TIME_DIALOG_ID = 1112;
    private TextView offTimeView;
    private int offTimeHour = 12;
    private int offTimeMin = 0;


//================================================================================
// Broadcast recieved logic
//================================================================================
    /**
     * Broadcast receiver which forces all view elements to be updated.
     */
    public class SettingsReceiver extends BroadcastReceiver {

        public SettingsReceiver() {
        }

        @Override
        public void onReceive(Context context, Intent intent) {
            /**
             * Gathers the current securty system information from the background service,
             * and updates all UI elements with the latest value.
             */
            Log.i("ControlFragment","Received message, updating view.");
            SecuritySystem secState = mService.getSecuritySystemState();
            updateView(secState);
        }
    }

    public void updateView(SecuritySystem secState)
    {
        if (secState.light_on_hour != -1 && secState.light_on_min != -1){
            onTimeView.setText(getTimeString(secState.light_on_hour, secState.light_on_min));
        }
        if (secState.light_off_hour != -1 && secState.light_off_min != -1){
            offTimeView.setText(getTimeString(secState.light_off_hour, secState.light_off_min));
        }
        if (secState.selected_audio_clip != -1){
            spinner.setSelection(secState.selected_audio_clip);
            update_from_broadcast = true;
        }

    }

//================================================================================
// Service Binding Logic
//================================================================================
    /** Defines callbacks for service binding, passed to bindService() */
    private ServiceConnection connection = new ServiceConnection() {

        @Override
        public void onServiceConnected(ComponentName className,
                                       IBinder service) {
            // We've bound to LocalService, cast the IBinder and get LocalService instance
            TCPService.LocalBinder binder = (TCPService.LocalBinder) service;
            mService = binder.getService();
            mBound = true;
        }

        @Override
        public void onServiceDisconnected(ComponentName arg0) {
            mBound = false;
        }
    };


//================================================================================
// Native Fragment Implementations
//================================================================================
    public static SettingsFragment newInstance(int index) {
        SettingsFragment fragment = new SettingsFragment();
        Bundle bundle = new Bundle();
        fragment.setArguments(bundle);
        return fragment;
    }

    public void onItemSelected(AdapterView<?> parent, View view,
                               int pos, long id) {
        if (mService != null) {
            //Finish line Hack
            mService.securitySysState.selected_audio_clip = pos;
            mService.sendSetStateToSystem();
            //Original Code
            /*
            if (! update_from_broadcast) {
                mService.securitySysState.selected_audio_clip = pos;
                mService.sendSetStateToSystem();
            }
            else{
                update_from_broadcast= false;
            }
             */
        }
    }

    public void onNothingSelected(AdapterView<?> parent) {
        // Another interface callback
    }


    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {

        binding = SettingsFragmentBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        // OnTime Setup
        onTimeView = binding.lightOnScheduleTime;
        onTimeView.setText("Unknown");
        onTimeView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createdDialog(LIGHTS_ON_TIME_DIALOG_ID).show();
            }
        });

        // Off time setup
        offTimeView = binding.lightOffScheduleTime;
        offTimeView.setText("Unknown");
        offTimeView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createdDialog(LIGHTS_OFF_TIME_DIALOG_ID).show();
            }
        });

        // Setup Dropdown menu
        spinner = binding.alarmNoiseDropDown;
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(globalContext,
                R.array.alarm_sounds_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        spinner.setAdapter(adapter);

        spinner.setOnItemSelectedListener(this);
        return root;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        globalContext = this.getActivity();
        super.onCreate(savedInstanceState);

        // Bind to LocalService
        Intent intent = new Intent(globalContext, TCPService.class);
        globalContext.bindService(intent, connection, Context.BIND_AUTO_CREATE);

        // Setup Broadcast receiver
        IntentFilter filter = new IntentFilter("settings_data");
        SettingsFragment.SettingsReceiver receiver = new SettingsReceiver();
        globalContext.registerReceiver(receiver, filter);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
//================================================================================
// Time Dialog Function
//================================================================================
    protected Dialog createdDialog(int id) {
        switch (id) {
            case LIGHTS_ON_TIME_DIALOG_ID:
                return new TimePickerDialog(globalContext, onTimePickerListener, onTimeHour, onTimeMin, false);
            case LIGHTS_OFF_TIME_DIALOG_ID:
                return new TimePickerDialog(globalContext, offTimePickerListener, offTimeHour, offTimeMin, false);
        }
        return null;
    }

    private TimePickerDialog.OnTimeSetListener onTimePickerListener = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hourOfDay, int minutes) {
            // Update UI Components
            onTimeHour = hourOfDay;
            onTimeMin = minutes;
            onTimeView.setText(getTimeString(onTimeHour, onTimeMin));

            // Inform Security System of change
            mService.securitySysState.light_on_min = minutes;
            mService.securitySysState.light_on_hour = hourOfDay;
            mService.sendSetStateToSystem();
        }
    };
    private TimePickerDialog.OnTimeSetListener offTimePickerListener = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hourOfDay, int minutes) {
            // Update UI Components
            offTimeHour = hourOfDay;
            offTimeMin = minutes;
            offTimeView.setText(getTimeString(offTimeHour, offTimeMin));
            // Inform Security System of change
            mService.securitySysState.light_off_min = minutes;
            mService.securitySysState.light_off_hour = hourOfDay;
            mService.sendSetStateToSystem();        }
    };
    private static String utilTime(int value) {
        if (value < 10) return "0" + String.valueOf(value);
        else return String.valueOf(value);
    }

    private String getTimeString(int hours, int mins) {
        String timeSet = "";
        if (hours > 12) {
            hours -= 12;
            timeSet = "PM";
        } else if (hours == 0) {
            hours += 12;
            timeSet = "AM";
        } else if (hours == 12)
            timeSet = "PM";
        else
            timeSet = "AM";
        String minutes = "";
        if (mins < 10)
            minutes = "0" + mins;
        else
            minutes = String.valueOf(mins);
        String aTime = new StringBuilder().append(hours).append(':').append(minutes).append(" ").append(timeSet).toString();
//        view.setText(aTime);
        return aTime;

    }


}