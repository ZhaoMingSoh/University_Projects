import java.io.Serializable;

public class Message implements Serializable{
    public String message_type = null;
    public int source_id = 0;
    public double proposal_id = 0.0;
    public double accepted_proposal_id = 0.0;
    public int proposal_val = 0;
    public boolean bool_accepted_proposal = false;

    public Message(String message_type, int source_id, double proposal_id, double accepted_proposal_id, int proposal_val, boolean bool_accepted_proposal){
        this.message_type = message_type;
        this.source_id = source_id;
        this.proposal_id = proposal_id;
        this.accepted_proposal_id = accepted_proposal_id;
        this.proposal_val = proposal_val;
        this.bool_accepted_proposal = bool_accepted_proposal;
    }
}
