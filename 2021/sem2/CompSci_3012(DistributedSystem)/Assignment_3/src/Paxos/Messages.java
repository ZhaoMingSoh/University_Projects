package Paxos;

import java.awt.*;
import java.io.Serializable;

public class Messages implements Serializable {
    String member_Type;
    String member_name;
    int prepare_Order = 0;

    // Prepare ID
    String message_Type;
    double id = 0;
    int propose_val = 0;

    // Initial Member Message to the Paxos Server - to announce its name, type, instances and if the member happens to be M1,M2 or M3
    // then also include the order in which M1,M2 or M3 will start in the prepare() phase.
    public Messages(String message_Type, String member_name, String member_Type, int prepare_Order){
        this.message_Type = message_Type;
        this.member_name = member_name;
        this.member_Type = member_Type;
        this.prepare_Order = prepare_Order;
    }

    // The messages that are sent after the initialization between Members and Paxos Server
    public Messages(String message_Type, double id, int propose_val){
        this.message_Type = message_Type;
        this.id = id;
        this.propose_val = propose_val;
    }

    public String getType(){
        return member_Type;
    }

    public String getMember_name(){
        return member_name;
    }


    public int getPrepare_Order(){
        return prepare_Order;
    }

    // The messages that are sent after the initialization between Members and Paxos Server
    public String getMessage_Type(){
        return message_Type;
    }

    public double getId(){
        return id;
    }

    public int getPropose_val(){
        return propose_val;
    }
}
