package com.example.securitysystemapp.ui.main;

import static android.app.Service.START_REDELIVER_INTENT;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import com.example.securitysystemapp.SecuritySystem;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;


public class TCPService extends Service {

//================================================================================
// class member variables
//================================================================================
    // Server Information
    public static final String START_SERVER = "startserver";
    public static final int SERVERPORT = 5000;
    private static final String SERVER_IP = "192.168.0.109";
    Thread connectionThread;
    public Socket clientSocket;

    // System State
    SecuritySystem securitySysState;

//================================================================================
// Service start up function
//================================================================================
    public TCPService() {

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        securitySysState = new SecuritySystem(this);
        Log.i("onStartCommand", "Starting Client Thread");
        this.connectionThread = new Thread(new ConnectionThread());
        this.connectionThread.start();
        return START_REDELIVER_INTENT;
    }


//================================================================================
// Binding Information
//================================================================================
    // Binder given to clients
    private final IBinder binder = new LocalBinder();
    /**
     * Class used for the client Binder.  Because we know this service always
     * runs in the same process as its clients, we don't need to deal with IPC.
     */
    public class LocalBinder extends Binder {
        TCPService getService() {
            // Return this instance of LocalService so clients can call public methods
            return TCPService.this;
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }
//================================================================================
// Connection Thread
//================================================================================
    class ConnectionThread implements Runnable {

        private PrintWriter output;
        Thread recThread;
        @Override
        public void run() {
            Log.i("ConnectionThread", "Starting Connection Thread");
            while(true) {

                boolean connectAttempt = (clientSocket == null);
//                if (!connectAttempt)
//                {
//                    output.println("heartbeat");
//                    if (output.checkError())
//                    {
//                        connectAttempt = true;
//                    }
//                }

                if (connectAttempt) {
                    try {
                        Log.i("ConnectionThread", "Attempting Connection to server");
                        InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
                        clientSocket = new Socket(serverAddr, SERVERPORT);

                        Log.i("ConnectionThread", "Connection Established");
                        this.output = new PrintWriter(clientSocket.getOutputStream(), true);

                        // Start thread

                        if (recThread != null) {
                            Log.i("ConnectionThread", "Stopping Receiver Thread");
                            recThread.stop();
                        }
                        Log.i("ConnectionThread", "Starting Receiver Thread");
                        RecieverRunnable recieverRunnable = new RecieverRunnable(clientSocket);
                        Thread recThread = new Thread(recieverRunnable);
                        recThread.start();
                    } catch (UnknownHostException e1) {
                        e1.printStackTrace();
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    } catch (Exception e) {
                        Log.i("ConnectionThread", "Something else went wrong");
                    }
                }

                // On retry connection every few seconds
                try {
                    Log.i("ConnectionThread", "Sleeping...");
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

//================================================================================
// Receiver Thread
//================================================================================
    class RecieverRunnable implements Runnable {

        private Socket clientSocket;

        private BufferedReader input;

        public RecieverRunnable(Socket clientSocket) {
            this.clientSocket = clientSocket;
            try {
                this.input = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run() {
            while(true) {
                try {
                    String result = input.readLine();
                    Log.i("RecieverRunnable",result);
                    securitySysState.setStateWithReceivedPacket(result);

                    // send broadcast
                    Intent control_intent = new Intent();
                    control_intent.setAction("control_data");
                    sendBroadcast(control_intent);

                    // send broadcast of settings
                    Intent settings_intent = new Intent();
                    settings_intent.setAction("settings_data");
                    sendBroadcast(settings_intent);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

//================================================================================
// Sender Thread
//================================================================================
    class SenderThread implements Runnable {
        private Socket clientSocket;
        private PrintWriter output;

        String data;

        public SenderThread(Socket clientSocket, String send_data) {
            this.clientSocket = clientSocket;
            this.data = send_data;
            try {
                output = new PrintWriter(clientSocket.getOutputStream(), true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run() {
            Log.i("SenderRunnable",this.data);
            output.println(this.data);
        }
    }

//================================================================================
// Public Methods for Users of service to call
//================================================================================
    public SecuritySystem getSecuritySystemState()
    {
        return securitySysState;
    }

    public void sendDataToSystem(String dataToSend) {
        SenderThread senderThread = new SenderThread(clientSocket, dataToSend);
        new Thread(senderThread).start();
    }

    public void sendSetStateToSystem() {
        String dataToSend = securitySysState.getDataToSend();
        SenderThread senderThread = new SenderThread(clientSocket, dataToSend);
        new Thread(senderThread).start();
    }

}
