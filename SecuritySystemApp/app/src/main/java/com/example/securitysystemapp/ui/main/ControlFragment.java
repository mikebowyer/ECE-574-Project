package com.example.securitysystemapp.ui.main;

import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.securitysystemapp.R;
import com.example.securitysystemapp.SecuritySystem;
import com.example.securitysystemapp.databinding.ControlFragmentBinding;
import com.example.securitysystemapp.databinding.FragmentMainBinding;

/**
 * A placeholder fragment containing a simple view.
 */
public class ControlFragment extends Fragment {
    TCPService mService;
    private static final String ARG_SECTION_NUMBER = "section_number";

    private PageViewModel pageViewModel;
    private ControlFragmentBinding binding;
    private Context globalContext = null;

    boolean mBound = false;
    public class MyReceiver extends BroadcastReceiver {

        public MyReceiver() {
        }

        @Override
        public void onReceive(Context context, Intent intent) {
            // Implement code here to be performed when
            // broadcast is detected
            Log.i("ControlFragment","Received message, updating view.");
            SecuritySystem secState = mService.getSecuritySystemState();
            updateView(secState);
        }
    }

    public void updateView(SecuritySystem secState)
    {
        if (secState.alarm_armed == 1)
        {
            binding.alarmToggleButton.setChecked(true);
            binding.alarmToggleButton.setText("Alarm Armed: On");
        }
        else
        {
            binding.alarmToggleButton.setChecked(false);
            if (secState.alarm_armed == 0)
            {
                binding.alarmToggleButton.setText("Alarm Armed: Off");
            }
            else
            {
                binding.alarmToggleButton.setText("Alarm Armed: Unknown");
            }
        }
    }
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

    public static ControlFragment newInstance(int index) {
        ControlFragment fragment = new ControlFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Bind to LocalService
        globalContext = this.getActivity();
        Intent intent = new Intent(globalContext, TCPService.class);
        globalContext.bindService(intent, connection, Context.BIND_AUTO_CREATE);

        //
        IntentFilter filter = new IntentFilter("recieved_new_data");
        MyReceiver receiver = new MyReceiver();
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
        alarmToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                mService.sendDataToSystem("FromControl!");
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