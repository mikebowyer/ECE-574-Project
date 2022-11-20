package com.example.securitysystemapp.ui.main;

import android.app.Dialog;
import android.app.TimePickerDialog;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.TimePicker;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.securitysystemapp.R;
import com.example.securitysystemapp.databinding.ControlFragmentBinding;
import com.example.securitysystemapp.databinding.FragmentMainBinding;
import com.example.securitysystemapp.databinding.SettingsFragmentBinding;

/**
 * A placeholder fragment containing a simple view.
 */
public class SettingsFragment extends Fragment {
    // Services
    TCPService mService;
    boolean mBound = false;
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

    private static final String ARG_SECTION_NUMBER = "section_number";
    private Context globalContext = null;

    // On Time Settings
    static final int LIGHTS_ON_TIME_DIALOG_ID = 1111;
    private TextView onTimeView;
    private int onTimeHour;
    private int onTimeMin;

    // On Time Settings
    static final int LIGHTS_OFF_TIME_DIALOG_ID = 1112;
    private TextView offTimeView;
    private int offTimeHour;
    private int offTimeMin;

//    private PageViewModel pageViewModel;
    private SettingsFragmentBinding binding;

    public static SettingsFragment newInstance(int index) {
        SettingsFragment fragment = new SettingsFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }
    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {

        binding = SettingsFragmentBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        onTimeView = binding.lightOnScheduleTime;
        onTimeView.setText("Extracting from security system...");
        onTimeView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createdDialog(LIGHTS_ON_TIME_DIALOG_ID).show();
            }
        });

        offTimeView = binding.lightOffScheduleTime;
        offTimeView.setText("Extracting from security system...");
        offTimeView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createdDialog(LIGHTS_OFF_TIME_DIALOG_ID).show();
            }
        });
        return root;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        globalContext = this.getActivity();
        super.onCreate(savedInstanceState);

        // Bind to LocalService
        Intent intent = new Intent(globalContext, TCPService.class);
        globalContext.bindService(intent, connection, Context.BIND_AUTO_CREATE);

//        pageViewModel = new ViewModelProvider(this).get(PageViewModel.class);
//        int index = 1;
//        if (getArguments() != null) {
//            index = getArguments().getInt(ARG_SECTION_NUMBER);
//        }
//        pageViewModel.setIndex(index);

    }
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
            onTimeHour = hourOfDay;
            onTimeMin = minutes;
            onTimeView.setText(getTimeString(onTimeHour, onTimeMin));

            String result =  mService.getMyString();
            Log.i("OUTPUT",result);
            mService.sendDataToSystem("Hi Dad!");
//            SharedPreferences.Editor editor = sharedpreferences.edit();
//            editor.putInt(StartTimeHour, hr);
//            editor.putInt(StartTimeMin, min);
//            editor.commit();
        }
    };
    private TimePickerDialog.OnTimeSetListener offTimePickerListener = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hourOfDay, int minutes) {
            // TODO Auto-generated method stub
            offTimeHour = hourOfDay;
            offTimeMin = minutes;
            offTimeView.setText(getTimeString(offTimeHour, offTimeMin));
//            SharedPreferences.Editor editor = sharedpreferences.edit();
//            editor.putInt(StartTimeHour, hr);
//            editor.putInt(StartTimeMin, min);
//            editor.commit();
        }
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



    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}