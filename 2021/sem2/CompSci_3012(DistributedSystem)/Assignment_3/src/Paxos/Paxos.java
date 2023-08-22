package Paxos;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;

public class Paxos {
    public static int paxos_count = 0;
    public static int number_Of_Proposers = 0;
    public static int temp_num = 0;
    public static int number_Of_Members = 0;
    public static boolean bool_Consensus = false;
    // LinkedListHashMap that stores each Member thread such that the server can know who is the proposer or acceptor
    public static Map<String, ArrayList<Object>> members_Thread_Map = new LinkedHashMap<>();
    public static ArrayList<Paxos_Handler> member_Threads = new ArrayList<>();
    public static ArrayList<ObjectOutputStream> outputStreams = new ArrayList<>();

    public static void main(String[] args){
        try {
            // Create a ServerSocket with a specific port
            ServerSocket Paxos = new ServerSocket(9090);
            while(true) {
                // listens for client connection request
                Socket client = Paxos.accept();
                // Once a client is accepted and connected to the ServerSocket, invoke a thread to handle the connected client
                Paxos_Handler client_thread = new Paxos_Handler(client);
                member_Threads.add(client_thread);
                number_Of_Members++;
                client_thread.start();
            }
        }catch (IOException e){
            e.printStackTrace();
        }
    }


    public static class Paxos_Handler extends Thread{
        Socket client = null;
        ObjectOutputStream write_Members;

        public Paxos_Handler(Socket client){
            this.client = client;
        }

        public void run(){
            try{
                write_Members = new ObjectOutputStream(client.getOutputStream());
                ObjectInputStream read_Members = new ObjectInputStream(client.getInputStream());

                // If a member is connected to the Paxos Server for the first time (indicated by the "instance" val)
                Messages member_Msg = null;
                System.out.println("[Paxos Server] is connected to a Member.");

                while(true){
                    member_Msg = (Messages) read_Members.readObject();
                    if(member_Msg.getMessage_Type().equals("Connected First Time")){
                        if (member_Msg.getType().equals("Proposer")) {
                            number_Of_Proposers++;
                        }
                        ArrayList<Object> store_member_Info = new ArrayList<>();
                        store_member_Info.add(currentThread());
                        store_member_Info.add(member_Msg.getType());
                        store_member_Info.add(member_Msg.getPrepare_Order());
                        members_Thread_Map.put(member_Msg.getMember_name(), store_member_Info);
                    }
                    // Inform Proposers to start the Paxos Algorithm
                    if(paxos_count == 0 && members_Thread_Map.size() >= 3) {
                        for (Paxos_Handler thread : member_Threads) {
                            Messages broadcast = new Messages("Start Prepare", 0.0, 0);
                            thread.write_Members.writeObject(broadcast);
                            write_Members.flush();
                        }
                        paxos_count++;
                    }else if(paxos_count == 1 && members_Thread_Map.size() >= 3){
                        if(member_Msg.getMessage_Type().equals("Prepare")){
                            for (Paxos_Handler thread : member_Threads) {
                                thread.write_Members.writeObject(member_Msg);
                                write_Members.flush();
                            }
                        }
                        paxos_count++;
                    }



                }




//                while(bool_Consensus == false) {
//                    if (number_Of_Members >= 3 && paxos_count == 0) {
//                        // Server will tell the Proposer to start sending their prepare message to other members including itself
//                        ArrayList<Paxos_Handler> proposer_Threads = new ArrayList<>();
//                        String curr_Thread = currentThread().getName();
//                        Messages start_msg = new Messages("Start Prepare Msg");
//                        for (Map.Entry<String, ArrayList<Object>> entry : members_Thread_Map.entrySet()) {
//                            if ((int) entry.getValue().get(2) == 1) {
//                                Thread one = (Thread) entry.getValue().get(0);
//                                if(curr_Thread.equals(one.getName())){
//                                    write_Members.writeObject(start_msg);
//                                    write_Members.flush();
//                                    break;
//                                }
//                            } else if ((int) entry.getValue().get(2) == 2) {
//                                Thread one = (Thread) entry.getValue().get(0);
//                                if(curr_Thread.equals(one.getName())){
//                                    write_Members.writeObject(start_msg);
//                                    write_Members.flush();
//                                    break;
//                                }
//                            } else if ((int) entry.getValue().get(2) == 3) {
//                                Thread one = (Thread) entry.getValue().get(0);
//                                if(curr_Thread.equals(one.getName())){
//                                    write_Members.writeObject(start_msg);
//                                    write_Members.flush();
//                                    break;
//                                }
//                            }
//                        }
//                        paxos_count++;
//
//                    }else if(paxos_count == 1){
//                        // Phase 1: Proposer will send Prepare Msg to all members including itself
//                        Messages member_Msg_2 = (Messages) read_Members.readObject();
//                        System.out.println(member_Msg_2.getMessage_Type()+" "+member_Msg_2.getId()+" "+member_Msg_2.propose_val);
//
//                    }
//
//                }

//                while(true) {
//                    Messages member_Msg_2 = (Messages) read_Members.readObject();
//                    if (member_Msg_2 == null) {
//                        break;
//                    }
//                    if (paxos_count == 0) {
//                        // If a member is connected to the Paxos Server for the first time (indicated by the "instance" val)
//                        for (Paxos_Handler thread : member_Threads) {
//                            Messages broadcast = new Messages("Start Prepare Msg");
//                            thread.write_Members.writeObject(broadcast);
//                            write_Members.flush();
//                        }
//                        paxos_count++;
//                    } else if (paxos_count == 1) {
//                        System.out.println(member_Msg.getId());
//                    }
//
//                    System.out.println("Number of Proposers : " + number_Of_Proposers);
//
//                    Iterator<String> iterator = members_Thread_Map.keySet().iterator();
//                    while (iterator.hasNext()) {
//                        String key = iterator.next();
//                        System.out.println(key);
//                    }
//
//                    for (int i = 0; i < member_Threads.size(); i++) {
//                        System.out.println(member_Threads.get(i).getName());
//                    }
//
//                }



            }catch (EOFException e){
                System.out.println("----------------------[Disconnection]-----------------------");
                String curr_Thread = currentThread().getName();
                for(int i=0; i<member_Threads.size(); i++){
                    if(member_Threads.get(i).getName().equals(curr_Thread)){
                        member_Threads.remove(i);
                        break;
                    }
                }
//                for(Map.Entry<String, String> entry : members_Thread_Map.entrySet()){
//                    if(entry.getValue().contains(curr_Thread)){
//                        System.out.println(entry.getKey()+" has disconnected.");
//                        members_Thread_Map.remove(entry.getKey());
//                        break;
//                    }
//                }
                System.out.println("-------------------------------------------------------------");
            }
            catch(Exception e){
                e.printStackTrace();
            }
        }
    }

    public static class Paxos_Writer extends Thread{

    }



}
