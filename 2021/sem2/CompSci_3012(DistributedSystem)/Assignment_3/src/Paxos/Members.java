package Paxos;

import java.io.*;
import java.net.Socket;

public class Members {
    String paxos_DNS = "";
    int paxos_port = 0;
    Socket paxos_Server = null;
    ObjectInputStream read_Obj = null;
    ObjectOutputStream write_Obj = null;

    String member_Type = "";
    String member_Name = "";  // Member's name where M1-M3 are the proposers and M4-M9 are the acceptors.
    int member_Number = 0;

    int prepare_Order = 0; // Proposer
    public static double p_ID = 0.0; // Proposer
    public static int temp_ID = 0; // Proposer
    int p_Val = 0; // Proposer
    double a_Max_ID = 0.0; // Acceptor and Proposer
    int accepted_Value = 0; // Acceptor

    public Members(String server_Name, int port, int member_Num, String member_Type, int prepare_Order){
        this.paxos_DNS = server_Name;
        this.paxos_port = port;
        this.member_Number = member_Num;
        this.member_Name = "M"+member_Num;
        this.member_Type = member_Type;
        this.prepare_Order = prepare_Order;
    }

    public void run(){
        try {
            paxos_Server = new Socket(paxos_DNS, paxos_port);
            write_Obj = new ObjectOutputStream(paxos_Server.getOutputStream());
            read_Obj = new ObjectInputStream(paxos_Server.getInputStream());

            // The first time a Member node is connected to the Paxos Server, immediately sends its own Name, type, instances and (order
            // in which the proposer will start the algo) to the Paxos Server
            Messages to_Paxos = new Messages("Connected First Time",member_Name, member_Type, prepare_Order);
            write_Obj.writeObject(to_Paxos);
            write_Obj.flush();

            // This is where each member will receive messages from the Paxos Server
            while(true){
                Messages obj = (Messages) read_Obj.readObject();
                if(obj.getMessage_Type().equals("Start Prepare")){
                    if(member_Type.equals("Proposer")) {
                        temp_ID++;
                        String decimal = String.valueOf(temp_ID) + "." + String.valueOf(member_Number);
                        p_ID = Double.valueOf(decimal);
                        Messages new_msg = new Messages("Prepare", p_ID, p_Val);
                        write_Obj.writeObject(new_msg);
                        write_Obj.flush();
                    }else{
                        continue;
                    }
                }
                if(obj.getMessage_Type().equals("Prepare")){
                    if(member_Type.equals("Proposer")) {
                        continue;
                    }else{
                        double prepare_ID = obj.getId();
                        if (prepare_ID > a_Max_ID) {
                            a_Max_ID = prepare_ID;
                            Messages promise = new Messages("Promise", a_Max_ID, accepted_Value);
                            write_Obj.writeObject(promise);
                            write_Obj.flush();
                        } else {

                        }
                    }
                }

            }
        }catch(Exception e){
            e.printStackTrace();
        }finally {
        }
    }

    public static void main(String[] args){
        int member_Num = Integer.parseInt(args[0]);
        String member_Type = args[1];

        System.out.println("[M"+member_Num+"] is connecting to the Paxos Server ......");
        Members M = new Members("localhost", 9090 , member_Num, member_Type, Integer.parseInt(args[2]));
        System.out.println("[M"+member_Num+"] is connected to the Paxos Server.");
        M.run();
    }

}
