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
    public static final int SERVERPORT = 8080;

    // Server Info
    private static final String SERVER_IP = "192.168.0.109";

    Thread serverThread;
    Thread clientThread;
    ServerSocket serverSocket;
    Socket clientSocket;

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
            try {
                InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

                clientSocket = new Socket(serverAddr, SERVERPORT);
                Log.i("ClientThread", "Connection Established");
            } catch (UnknownHostException e1) {
                e1.printStackTrace();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            while (!Thread.currentThread().isInterrupted()) {
                Log.i("ClientThread", "Starting Comms Thread");
                CommunicationThread commThread = new CommunicationThread(clientSocket);
                new Thread(commThread).start();
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

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run() {

            try {

                String read = input.readLine();

                //update ui
                //best way I found is to save the text somewhere and notify the MainActivity
                //e.g. with a Broadcast
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }
}
