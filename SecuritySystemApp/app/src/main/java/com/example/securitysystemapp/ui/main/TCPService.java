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
    SecuritySystem securitySysState;
    public TCPService() {

    }
/*
        Member Variables
 */
    // Server Information
    public static final String START_SERVER = "startserver";
    public static final int SERVERPORT = 5000;
    private static final String SERVER_IP = "192.168.0.109";
    Thread connectionThread;
    public Socket clientSocket;

    // Binder given to clients
    private final IBinder binder = new LocalBinder();

    // Interpretted  Information
    String myString = "dumb";

    //called when the services starts
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        securitySysState = new SecuritySystem();
        Log.i("onStartCommand", "Starting Client Thread");
        this.connectionThread = new Thread(new ConnectionThread());
        this.connectionThread.start();
        return START_REDELIVER_INTENT;
    }

/*
        Binding Information
 */


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


/*
        Threads
 */
    class ConnectionThread implements Runnable {

        private PrintWriter output;
        Thread recThread;
        @Override
        public void run() {
            Log.i("ConnectionThread", "Starting Connection Thread");
            while(true) {

                boolean connectAttempt = (clientSocket == null);
                if (!connectAttempt)
                {
                    output.println("heartbeat");
                    if (output.checkError())
                    {
                        connectAttempt = true;
                    }
                }

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
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

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

/*
        Public Interface
 */
    public String getMyString() {
        return myString;
    }

    /** method for clients */
    public void sendDataToSystem(String dataToSend) {
        SenderThread senderThread = new SenderThread(clientSocket, dataToSend);
        new Thread(senderThread).start();
    }

}
