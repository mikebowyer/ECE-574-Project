package com.example.securitysystemapp.ui.main;

import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.graphics.Color;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.ToggleButton;

import androidx.annotation.ColorInt;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.example.securitysystemapp.SecuritySystem;
import com.example.securitysystemapp.databinding.ControlFragmentBinding;
import com.pes.androidmaterialcolorpickerdialog.ColorPicker;
import com.pes.androidmaterialcolorpickerdialog.ColorPickerCallback;


/**
 * The fragment for the Control tab in the main activity.
 */
public class ControlFragment extends Fragment {

//================================================================================
// class member variables
//================================================================================
    // Background Service information
    TCPService mService;
    boolean mBound = false;

    // UI Elements & Context Info
    private ControlFragmentBinding binding;
    private Context globalContext = null;

    // Color Picker
    private View mColorPreview;

//================================================================================
// class broadcast reception
//================================================================================
    /**
     * Broadcast receiver which forces all view elements to be updated.
     */
    public class ControlReciever extends BroadcastReceiver {

        public ControlReciever() {
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
        switch(secState.alarm_armed) {
            case 1:
                binding.alarmToggleButton.setChecked(true);
//                binding.alarmToggleButton.setText("Alarm Armed: On");
                break;
            case 0:
                binding.alarmToggleButton.setChecked(false);
                break;
            default:
                break;
        }
        switch(secState.lights) {
            case 1:
                binding.lightsToggleButton.setChecked(true);
//                binding.alarmToggleButton.setText("Alarm Armed: On");
                break;
            case 0:
                binding.lightsToggleButton.setChecked(false);
                break;
            default:
                break;
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


            if(mService != null){
                mBound = true;
                Log.i("service-bind", "Service is bonded successfully!");


                //do whatever you want to do after successful binding
            }
            else
            {
                Log.e("service-bind", "Service is bonded successfully!");
            }
        }

        @Override
        public void onServiceDisconnected(ComponentName arg0) {
            mBound = false;
        }
    };

//================================================================================
// Native Fragment Implementations
//================================================================================
    public static ControlFragment newInstance(int index) {
        ControlFragment fragment = new ControlFragment();
        Bundle bundle = new Bundle();
        fragment.setArguments(bundle);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Bind to LocalService
        globalContext = this.getActivity();
        Intent intent = new Intent(globalContext, TCPService.class);
        globalContext.bindService(intent, connection, Context.BIND_AUTO_CREATE);

        // Setup Broadcast reciever
        IntentFilter filter = new IntentFilter("control_data");
        ControlReciever receiver = new ControlReciever();
        globalContext.registerReceiver(receiver, filter);


        super.onCreate(savedInstanceState);


    }

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {

        binding = ControlFragmentBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        // Setup Alarm toggle Button
        ToggleButton alarmToggle = binding.alarmToggleButton;
        alarmToggle.setText("Alarm Armed: Unknown");
        alarmToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked)
                {mService.securitySysState.alarm_armed = 1;}
                else{
                    mService.securitySysState.alarm_armed = 0;
                }
                mService.sendSetStateToSystem();
            }
        });

        // Setup Lights toggle button
        ToggleButton lightsToggle = binding.lightsToggleButton;
        lightsToggle.setText("Lights State: Unknown");
        lightsToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked)
                {mService.securitySysState.lights = 1;}
                else{
                    mService.securitySysState.lights = 0;
                }
                mService.sendSetStateToSystem();
            }
        });

        // Setup color selector
        mColorPreview = binding.previewSelectedColor;
//        mColorPreview.setBackgroundColor(100);
        mColorPreview.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final ColorPicker cp = new ColorPicker(getActivity(), 0, 0, 0);
                /* Show color picker dialog */
                cp.show();

                cp.enableAutoClose(); // Enable auto-dismiss for the dialog

                /* Set a new Listener called when user click "select" */
                cp.setCallback(new ColorPickerCallback() {
                    @Override
                    public void onColorChosen(@ColorInt int color) {
                        // Do whatever you want
                        // Examples
                        Log.d("Alpha", Integer.toString(Color.alpha(color)));
                        Log.d("Red", Integer.toString(Color.red(color)));
                        Log.d("Green", Integer.toString(Color.green(color)));
                        Log.d("Blue", Integer.toString(Color.blue(color)));

                        Log.d("Pure Hex", Integer.toHexString(color));
                        Log.d("#Hex no alpha", String.format("#%06X", (0xFFFFFF & color)));
                        Log.d("#Hex with alpha", String.format("#%08X", (0xFFFFFFFF & color)));

                        // If the auto-dismiss option is not enable (disabled as default) you have to manually dimiss the dialog
                        // cp.dismiss();
//                        int color_output = (Color.alpha(color) & 0xff) << 24 | (Color.red(color) & 0xff) << 16 | (Color.green(color) & 0xff) << 8 | (B & 0xff);
                        mColorPreview.setBackgroundColor(color);
                    }
                });
            }
        });


        final TextView textView = binding.sectionLabel;
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}