package com.example.securitysystemapp;

import android.content.Intent;
import android.os.Bundle;

import com.example.securitysystemapp.ui.main.TCPService;
import com.google.android.material.tabs.TabLayout;

import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import com.example.securitysystemapp.ui.main.SectionsPagerAdapter;
import com.example.securitysystemapp.databinding.ActivityMainBinding;

import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Setup Page Adapter and Tabs
        SectionsPagerAdapter sectionsPagerAdapter = new SectionsPagerAdapter(this, getSupportFragmentManager());
        ViewPager viewPager = binding.viewPager;
        viewPager.setAdapter(sectionsPagerAdapter);
        TabLayout tabs = binding.tabs;
        tabs.setupWithViewPager(viewPager);

        // Start TCP Comms
        Intent startServer = new Intent(this, TCPService.class);
        startServer.setAction(TCPService.START_SERVER);
        Log.i("MainActivity", "Starting TCP Service");
        startService(startServer);
    }
}