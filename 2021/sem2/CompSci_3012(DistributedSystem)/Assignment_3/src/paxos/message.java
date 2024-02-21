package paxos;

import java.io.Serializable;

public class message implements Serializable {
    String message_Type = "";
    int sender_Member_ID = 0;
    double unique_proposal_ID = 0.0;
    double accepted_unique_Proposal_ID = 0.0;
    int proposal_Value = 0;
    boolean bool_proposal_Accepted = false;

    public message(String message_Type, int sender_Member_ID, double unique_proposal_ID, double accepted_unique_Proposal_ID, int proposal_Value, boolean bool_proposal_Accepted){
        this.message_Type = message_Type;
        this.sender_Member_ID = sender_Member_ID;
        this.unique_proposal_ID = unique_proposal_ID;
        this.accepted_unique_Proposal_ID = accepted_unique_Proposal_ID;
        this.proposal_Value = proposal_Value;
        this.bool_proposal_Accepted = bool_proposal_Accepted;
    }

    public String getMessage_Type(){
        return message_Type;
    }

    public int getSender_Member_ID(){
        return sender_Member_ID;
    }

    public double getUnique_proposal_ID(){
        return unique_proposal_ID;
    }

    public double getAccepted_unique_Proposal_ID(){
        return accepted_unique_Proposal_ID;
    }

    public int getProposal_Value(){
        return proposal_Value;
    }

    public boolean getProposal_Accepted(){
        return bool_proposal_Accepted;
    }

}
