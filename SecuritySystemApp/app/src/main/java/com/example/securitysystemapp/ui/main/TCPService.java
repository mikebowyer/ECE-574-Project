package com.example.securitysystemapp.ui.main;

import static android.app.Service.START_REDELIVER_INTENT;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;

public class TCPService extends Service {
    public static final String START_SERVER = "startserver";
    public static final String STOP_SERVER = "stopserver";
    public static final int SERVERPORT = 5000;

    // Server Info
    private static final String SERVER_IP = "192.168.0.109";
//    private static final String SERVER_IP = "DESKTOP-9MIF63P";


    Thread serverThread;
    Thread clientThread;
    ServerSocket serverSocket;
    public Socket clientSocket;


    public TCPService() {

    }

    //called when the services starts
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        //action set by setAction() in activity

        Log.i("onStartCommand", "Starting Client Thread");
        this.clientThread = new Thread(new ClientThread());
        this.clientThread.start();

        return START_REDELIVER_INTENT;
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    class ClientThread implements Runnable {

        @Override
        public void run() {
            Log.i("ClientThread", "Starting Attempting Connection");

            while(clientSocket == null || !clientSocket.isConnected()){
                try {
                    InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

                    clientSocket = new Socket(serverAddr, SERVERPORT);
                    Log.i("ClientThread", "Connection Established");
                    Log.i("ClientThread", "Starting Comms Thread");
                    CommunicationThread commThread = new CommunicationThread(clientSocket);
                    new Thread(commThread).start();
                } catch (UnknownHostException e1) {
                    e1.printStackTrace();
                } catch (IOException e1) {
                    e1.printStackTrace();
                } catch (Exception e){
                    Log.i("ClientThread", "FUCK");
                }
            }
        }
    }

    class CommunicationThread implements Runnable {

        private Socket clientSocket;

        private BufferedReader input;

        public CommunicationThread(Socket clientSocket) {

            this.clientSocket = clientSocket;

            try {

                this.input = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
                String read = input.readLine();
                Log.i("ComsThread", read);

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run() {

            try {

                String read = input.readLine();
                Log.i("ComThread", "read");

                //update ui
                //best way I found is to save the text somewhere and notify the MainActivity
                //e.g. with a Broadcast
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }
}
