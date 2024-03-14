import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Members {
    public int id = 0;
    int port_num = 0;
    public String member_type = null;
    public String delay_type = null;
    boolean bool_consensus = false;
    
    // Socket attributes
    ServerSocket server_sock = null;

    // Proposer attributes
    int temp_id = 0;
    double proposal_ID = 0.0;
    int proposal_val = 0;
    double highest_id = -1.0;
    int highest_val = -1;

    public ArrayList<Message> promises = new ArrayList<>();
    public ArrayList<Message> accepts = new ArrayList<>();

    // Acceptor attributes
    boolean bool_accepted_proposal = false;
    double max_proposal_id = 0.0;
    double accepted_proposal_id = 0.0;
    int accepted_proposal_val = 0;

    public Members(int id, int port_num, String member_type, String delay_type){
        this.id = id;
        this.port_num = port_num;
        this.member_type = member_type;
        this.delay_type = delay_type;
        this.proposal_val = id;
    }   

    public void connect_members(){
        try{
            server_sock = new ServerSocket(this.port_num);

            while(bool_consensus == false){
                Socket client_sock = this.server_sock.accept();
                handle_client(client_sock);
            }

        }catch(Exception e){
            System.out.println("Error in either creating server sock for each members or error in establishing client socket connection.");
            System.out.println(e);
        }
    }

    public void handle_client(Socket client_sock){
        try{
            ObjectInputStream read_from = new ObjectInputStream(client_sock.getInputStream());
            Message client_data =(Message) read_from.readObject();

            /*
                Phase 1b : (Promise)
                Acceptors
                if (ID <= max_id)
                    do not respond (or respond with a "fail" message)
                else
                    max_id = ID     // save highest ID we've seen so far
                    if (proposal_accepted == true) // was a proposal already accepted?
                        respond: PROMISE(ID, accepted_ID, accepted_VALUE)
                    else
                        respond: PROMISE(ID)
             */
            if(client_data.message_type.equals("prepare")){
                double proposal_id = client_data.proposal_id;
                int source_id = client_data.source_id;

                if(proposal_id <= this.max_proposal_id){

                }else{
                    this.max_proposal_id = proposal_id;
                    Message promise_msg = null;
                    if(this.bool_accepted_proposal){
                        promise_msg = new Message("promise", this.id, proposal_id, this.accepted_proposal_id, this.accepted_proposal_val, this.bool_accepted_proposal);
                        send_message(source_id, promise_msg);
                    }else{
                        promise_msg = new Message("promise", this.id, proposal_id, 0.0, 0, false);
                        send_message(source_id, promise_msg);
                    }
                }
            }
            /* 
                Phase 2a : (Propose)
                Proposers
                did I receive PROMISE responses from a majority of acceptors?
                if yes
                    do any responses contain accepted values (from other proposals)?
                    if yes
                        val = accepted_VALUE    // value from PROMISE message with the highest accepted ID
                    if no
                        val = VALUE     // we can use our proposed value
                    send PROPOSE(ID, val) to at least a majority of acceptors

            */
            else if(client_data.message_type.equals("promise")){
                boolean response_bool = client_data.bool_accepted_proposal;
                double proposal_id = client_data.proposal_id;
                double accepted_proposal_id = client_data.accepted_proposal_id;
                int accepted_val = client_data.proposal_val;

                if(response_bool){
                    if(accepted_proposal_id > this.highest_id){
                        this.highest_id = accepted_proposal_id;
                        this.highest_val = accepted_val;
                    }
                }

                this.promises.add(client_data);
                
                if(this.promises.size() >= GlobalVariable.majority){
                    Message propose_msg = null;

                    if(response_bool){
                        propose_msg = new Message("propose", this.id, proposal_id, highest_id, highest_val, response_bool);
                        broadcast(propose_msg);
                    }else{
                        propose_msg = new Message("propose", this.id, proposal_id, 0.0, this.proposal_val, response_bool);
                        broadcast(propose_msg);
                    }
                }else{
                    this.prepare();
                }
            }
            /*
                Phase 2b : (Accept)
                Acceptors
                if (ID == max_id) // is the ID the largest I have seen so far?
                    proposal_accepted = true     // note that we accepted a proposal
                    accepted_ID = ID             // save the accepted proposal number
                    accepted_VALUE = VALUE       // save the accepted proposal data
                    respond: ACCEPTED(ID, VALUE) to the proposer and all learners
                else
                    do not respond (or respond with a "fail" message)
             */
            else if(client_data.message_type.equals("propose")){
                int source_id = client_data.source_id;
                double proposal_id = client_data.proposal_id;
                int proposal_val = client_data.proposal_val;
                Message accept_msg = null;

                if(proposal_id == this.max_proposal_id){
                    this.bool_accepted_proposal = true;
                    this.accepted_proposal_id = proposal_id;
                    this.accepted_proposal_val = proposal_val;
                    accept_msg = new Message("accept", this.id, proposal_id, proposal_id, proposal_val, bool_accepted_proposal);
                    send_message(source_id, accept_msg);
                }else{
                
                }

            }
            /*
                Last Phase : (Final)
                Proposers
                did I receive ACCEPT responses from a majority of acceptors?
                if yes,
                    consensus has been reached on the Accept(id, val)
                else,
                    re-propose ?
             */
            else if(client_data.message_type.equals("accept")){
                this.accepts.add(client_data);
                Message final_msg = null;
                int source_id = client_data.source_id;
                double final_id = client_data.proposal_id;
                int final_val = client_data.proposal_val;
                boolean bool_accepted_proposal = client_data.bool_accepted_proposal;

                if(this.accepts.size() > GlobalVariable.majority){
                    final_msg = new Message("final", this.id, final_id, final_id, final_val, bool_accepted_proposal);
                    send_message(source_id, final_msg);
                }else{
                    
                }
            }

        }catch(Exception e){
            System.out.println();
            System.out.println(e);
        }
    }

    /*
        Phase 1a : (Prepare)
        Proposers
            ID = cnt++;
            send PREPARE(ID)
     */
    public void prepare(){
        this.temp_id ++;
        String decimal = this.temp_id + "." + this.id;
        this.proposal_ID = Double.valueOf(decimal);
        Message prepare_msg = null;
        prepare_msg = new Message("prepare", this.id, this.proposal_ID, 0.0, 0, false);
        broadcast(prepare_msg);
    }

    public void broadcast(Message message){
        for(int member_id=1; member_id<=GlobalVariable.members; member_id++){
            if(member_id == this.id){
                continue;
            }else{
                send_message(member_id, message);
            }
        }
    }

    public void send_message(int member_id, Message message){
        try{
            if(message.message_type.equals("prepare")){
                System.out.println("[Phase 1a] M" + message.source_id + " -----> Prepare("+ message.proposal_id +") -----> "+ "M" + member_id );
            }else if(message.message_type.equals("promise")){
                if(message.bool_accepted_proposal){
                    System.out.println("[Phase 1b] M" + message.source_id + " -----> Promise("+ message.proposal_id + "," + message.accepted_proposal_id + "," + message.proposal_val + ") -----> "+ "M" + member_id );
                }else{
                    System.out.println("[Phase 1b] M" + message.source_id + " -----> Promise("+ message.proposal_id + "," + message.proposal_val + ") -----> "+ "M" + member_id );
                }
            }else if(message.message_type.equals("propose")){
                System.out.println("[Phase 2a] M" + message.source_id + " -----> Propose("+ message.proposal_id + "," + message.proposal_val + ") -----> "+ "M" + member_id );
            }else if(message.message_type.equals("accept")){
                System.out.println("[Phase 2b] M" + message.source_id + " -----> Accept("+ message.proposal_id + "," + message.proposal_val + ") -----> "+ "M" + member_id );
            }else if(message.message_type.equals("final")){
                System.out.println("[Phase 3a] M" + message.source_id + " -----> M" + message.proposal_val + " is the president! on "+ message.proposal_id +" -----> "+ "M" + member_id );
            }
            
            // Delays in sending messages
            if(this.delay_type.equals("immediate")){
                // do nothing
            }else if(this.delay_type.equals("medium")){
                Thread.sleep(2000);
            }else if(this.delay_type.equals("late")){
                Thread.sleep(3000);
            }

            int server_port_num = GlobalVariable.base_port + (member_id*100);
            Socket server_sock_ = new Socket("localhost", server_port_num);
            ObjectOutputStream write_To = new ObjectOutputStream(server_sock_.getOutputStream());
            write_To.writeObject(message);
            write_To.close();
            server_sock_.close();
        }catch(Exception e){
            System.err.println("Error in creating a socket connection to M" + this.id + " at (localhost," + GlobalVariable.base_port + (member_id * 100) + ")");
            System.out.println(e);
        }
    }
}   

