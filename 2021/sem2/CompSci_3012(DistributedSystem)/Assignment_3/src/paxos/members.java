package paxos;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class members {
    String member_Type = "";
    int member_ID = 0;
    int max_num_Member = 0;
    public String delay_Type = "";
    public boolean is_Offline = false;


    // Socket Connections Attributes
    ServerSocket memberAsServer = null;
    Socket otherMembers = null;
    int port_Num = 0;
    boolean bool_Consensus = false;

    public ArrayList<message> number_Of_Fail_Prepare = new ArrayList<>();

    // Proposer Attributes
    int temp_ID = 0;
    double proposal_ID = 0.0;
    int proposal_Val = 0;
    public ArrayList<message> number_Of_promises_Received = new ArrayList<>();
    public ArrayList<message> number_Of_accepted_Received = new ArrayList<>();

    // Acceptor Attributes
    double max_Proposal_ID = 0.0;
    double accepted_proposal_ID = 0;
    int accepted_proposal_Val = 0;
    boolean bool_accepted_val = false;
    boolean contain_Accepted_Val = false;

    // Consensus Attributes
    double final_Max_Proposal_ID = 0.0;
    int final_Proposal_Val = 0;
    double last_accepted_Proposal_ID = 0.0;
    String test_File_Path = "";
    String expected_Test_File_Path = "";


    public members(int member_ID, int port_Num, int max_num_Member, String member_Type, String delay_Type){
        this.member_ID = member_ID;
        this.port_Num = port_Num;
        this.max_num_Member = max_num_Member;
        this.member_Type = member_Type;
        this.delay_Type = delay_Type;
        this.proposal_Val = member_ID;
    }

    // Step 1:
    // 1. Connect each member object to a ServerSocket at a designated port number (6060 + (member_ID)*100)
    // 2. Once Connected, each member's ServerSocket will listen for other members Socket Connection ......
    public void connect_To_Other_Members(){
        try{

            memberAsServer = new ServerSocket(this.port_Num);

            while(bool_Consensus == false){
                otherMembers = memberAsServer.accept();
                receiving(otherMembers);

            }

            // Write the end results into the Test_Files located in the Testing Folder.
            try{
                this.test_File_Path = test.test_file_Path;
                this.expected_Test_File_Path = test.expected_Output_File_Path;
                File open_File_1 = new File(this.test_File_Path);
                File open_File_2 = new File(this.expected_Test_File_Path);
                if(open_File_1.exists()){
                    BufferedWriter write_To_File = new BufferedWriter(new FileWriter(open_File_1, true));
                    write_To_File.write("M"+this.member_ID + " final value is " + this.final_Proposal_Val + " from "+ this.last_accepted_Proposal_ID +" with proposal ID of " + this.final_Max_Proposal_ID + "\n");
                    write_To_File.close();
                }else{
                    System.out.println("Error : File at "+ this.test_File_Path + " does not exist.");
                }
                if(open_File_2.exists()){
                    BufferedWriter write_To_File = new BufferedWriter(new FileWriter(open_File_2, true));
                    write_To_File.write("M"+this.member_ID + " final value is " + this.final_Proposal_Val + " with proposal ID of " + this.final_Max_Proposal_ID + "\n");
                    write_To_File.close();
                }else{
                    System.out.println("Error : File at "+ this.expected_Test_File_Path + " does not exist.");
                }
            }catch (IOException e){
                System.err.println("Error : Unable to open file at "+ this.test_File_Path + " or " + this.expected_Test_File_Path + ".");
            }
        }catch (Exception e){
            System.err.println("Error in creating ServerSocket for "+ this.member_ID + " or " + " in connecting with other members ServerSocket.");
        }
    }

    // Step 2: Proposers M1-M3 will start sending prepare(unique_proposal_ID, null) message to all other members excluding itself.
    public void prepare() {
        number_Of_promises_Received.clear();
        temp_ID++;
        String decimal = temp_ID + "." + member_ID;
        proposal_ID = Double.valueOf(decimal);
        message prepareMsg = null;
        prepareMsg = new message("Prepare Msg", this.member_ID, this.proposal_ID, 0.0, 0, bool_accepted_val);
        sendToAll(prepareMsg, false);
        try{
            Thread.sleep(2000);
            if(number_Of_promises_Received.size() < ((max_num_Member-1)/2)+1 && !bool_Consensus){
                if(delay_Type.equals("medium")){
                    Thread.sleep(300);
                }else if(delay_Type.equals("late")){
                    Thread.sleep(600);
                }
                System.out.println("[Phase 1(a)] : M" + this.member_ID + " resend Prepare for " + this.proposal_ID);
                prepare();
            }
            else if(number_Of_promises_Received.size() > ((max_num_Member-1)/2)+1 && !bool_Consensus){
                if(delay_Type.equals("medium")){
                    Thread.sleep(300);
                }else if(delay_Type.equals("late")){
                    Thread.sleep(600);
                }
                String filler = "############";
                String space = "            ";
                System.out.println(filler + " [Phase 2(a)] : M" + this.member_ID + " received a majority of Promises. " + filler + "\n" +
                        filler + " M" + this.member_ID + " starts sending Propose Msg to all members. " + filler + "\n" +
                        space + "M" + this.member_ID + " ------------> Propose(" + this.proposal_ID + "," + this.proposal_Val + ")\n");
            }
        }catch (InterruptedException e){
            e.printStackTrace();
        }

    }

    public void propose(){

    }

    /*
        Broadcast the proposer's messages to all the other members. Depending on which phase the paxos algorithm is in:
        1. Phase 1(a): Proposers M1-M3 will only send prepare messages to all the other members excluding itself. (By setting bool_BroadCast = false)
        2. Phase 3(a): Proposers M1-M3 will send the final messages(confirms the final value and proposal_ID that reaches consensus) to all the other members including itself. (By setting bool_BroadCast = true)
     */
    public void sendToAll(message MsgObj, boolean bool_BroadCast){
        String filler = "############";
        String space = "            ";
        if(MsgObj.getMessage_Type().equals("Prepare Msg")) {
            System.out.println(filler + " [Phase 1(a)] : M" + MsgObj.getSender_Member_ID() + " starts sending Prepare Msg to all members. " + filler +
                    "\n" + space + "M" + MsgObj.getSender_Member_ID() + " ------------> Prepare(" + MsgObj.getUnique_proposal_ID() + "," + MsgObj.getProposal_Value() + ")\n");
        }else if(MsgObj.getMessage_Type().equals("Last Confirmed Msg")){
            System.out.println(filler + " M" + MsgObj.getSender_Member_ID() + " received a majority of Accepted(" + MsgObj.getUnique_proposal_ID() + "," + MsgObj.getProposal_Value() + ") " + filler + "\n" +
                    filler + " M" + MsgObj.getSender_Member_ID() + " starts sending Final Msg to all members. " +  filler );
        }

        if(bool_BroadCast == false) {
            for (int i = 1; i <= max_num_Member; i++) {
                if (i == this.member_ID) {
                    continue;
                } else {
                    send(i, MsgObj);
                }
            }
        }else{
            for (int i = 1; i <= max_num_Member; i++) {
                send(i, MsgObj);
            }
        }
    }

    /*
        Send messages from each member to all other members via connecting to their ServerSocket using Socket connections.
        1. Get the port number of the member that the current member wants to send messages to.
        2. Connect to the member ServerSocket via a member Socket connection.
        3. Extract the ObjectOutputStream from the member Socket and write the object into that stream.
     */
    public void send(int member_ID_to_send, message MsgObj){
        try{
            int member_port_num = 6060 + (member_ID_to_send*100);
            Socket member = new Socket("localhost", member_port_num);
            ObjectOutputStream write_To = new ObjectOutputStream(member.getOutputStream());
            write_To.writeObject(MsgObj);
            write_To.close();
            member.close();
        }catch(Exception e){
            System.err.println("Error in creating a Socket connection to M" + this.member_ID + " with port number " + (6060 + (this.member_ID) * 100) + " !!" );
        }
    }

    /*
        Step 3:
        This is where all members will receive and read messages that are sent from other members.
        1. A member will know when a message will arrive by listening for Socket connection from other members via its own ServerSocket accept() in connect_To_Other_Members().
        2. Once it is connected to a member Socket, it will extract the member's Socket ObjectInputStream to read from it.
        3. Then it will proceed to process the messages received.
     */
    public synchronized void receiving(Socket otherMembers_){
        try{
            ObjectInputStream read_from = new ObjectInputStream(otherMembers_.getInputStream());
            message MsgObj_From =(message) read_from.readObject();

            /*
                Phase 1(b): This is where All members (M1-M9) will receive prepare messages from proposers (M1-M3)
                1. The receiving member will check to see if the proposal_ID from the incoming messages is greater the max_proposal_ID.
                   a. If yes, then it will change its max_Proposal_ID = proposal_ID from the incoming messages.
                   b. If no, then it will send a fail prepare message to the corresponding proposer.
                        - Both will check to see if it has already accepted a val from a previous proposer with a lower proposal_ID
                            a. If yes, send a Promise(max_Proposal_ID, accepted_Proposal_ID, accepted_Proposal_Val) to the corresponding proposer.
                            b. If no, send a Promise(max_Proposal_ID, Proposal_Val) to the corresponding proposer.
             */
            if(MsgObj_From.getMessage_Type().equals("Prepare Msg")){
                int sender_Member_ID = MsgObj_From.getSender_Member_ID();
                double sender_uniqueProposal_ID = MsgObj_From.getUnique_proposal_ID();

                if(sender_uniqueProposal_ID > this.max_Proposal_ID){
                    max_Proposal_ID = sender_uniqueProposal_ID;
                    message promise_Msg = null;
                    if(bool_accepted_val ==  true){
                        System.out.println("[Phase 1(b)] : M" + this.member_ID + " sends Promise(" + sender_uniqueProposal_ID + "," + this.accepted_proposal_ID + "," + this.accepted_proposal_Val + ") ------------> M" + sender_Member_ID);
                        promise_Msg = new message("Promise Msg", this.member_ID, sender_uniqueProposal_ID, this.accepted_proposal_ID, this.accepted_proposal_Val, bool_accepted_val);
                    }else {
                        System.out.println("[Phase 1(b)] : M" + this.member_ID + " sends Promise(" + sender_uniqueProposal_ID + "," + 0 + ") ------------> M" + sender_Member_ID);
                        promise_Msg = new message("Promise Msg", this.member_ID, sender_uniqueProposal_ID, 0.0,0, bool_accepted_val);
                    }

                    if(delay_Type.equals("immediate")){
                        // no sleep
                    }else if(delay_Type.equals("medium")){
                        Thread.sleep(300);
                    }else if(delay_Type.equals("late")){
                        Thread.sleep(600);
                    }

                    if(!delay_Type.equals("never") || !is_Offline) {
                        send(sender_Member_ID, promise_Msg);
                    }
                }
                else{
                    if(bool_accepted_val ==  true){
                        System.out.println("[Phase 1(b)] : M" + this.member_ID + " *[fails]* to send Promise(" + sender_uniqueProposal_ID + "," + this.accepted_proposal_ID + "," + this.accepted_proposal_Val + ") ------------> M" + sender_Member_ID);
                    }else {
                        System.out.println("[Phase 1(b)] : M" + this.member_ID + " *[fails]* to send Promise(" + sender_uniqueProposal_ID + "," + 0 + ") ------------> M" + sender_Member_ID);
                    }
                }
            }
            /*
                Phase 2(a): This is where the Proposers (M1-M3) will receive Promise Msg from the other members.
                1. The proposer will check if the incoming Promise Msg exceeds the majority of the members.
                    a. If yes, It will check if the members that sent the Promise Msg had already accepted a Proposal Val in the past.
                        - If yes, It will change its current Proposal_Val into the already accepted Proposal Val.
                            - then proceed to send a Propose(max_Proposal_ID, Proposal_Val) Msg to the other members excluding itself.
                    b. If no, It will simply Ignore those messages.
             */
            else if(MsgObj_From.getMessage_Type().equals("Promise Msg")){
                int sender_Member_ID = MsgObj_From.getSender_Member_ID();
                double sender_uniqueProposal_ID = MsgObj_From.getUnique_proposal_ID();
                double sender_acceptedUnique_Proposal_ID = MsgObj_From.getAccepted_unique_Proposal_ID();
                boolean sender_bool_accepted_Val = MsgObj_From.getProposal_Accepted();
                int sender_proposal_Val = MsgObj_From.getProposal_Value();

                if(sender_uniqueProposal_ID == this.proposal_ID){
                    number_Of_promises_Received.add(MsgObj_From);
                    if(sender_bool_accepted_Val == true && !contain_Accepted_Val){
                        this.accepted_proposal_ID = sender_acceptedUnique_Proposal_ID;
                        this.proposal_Val = sender_proposal_Val;
                        contain_Accepted_Val = true;
                    }
                    System.out.println("[Phase 2(a)] : M" + this.member_ID + "receives Promise(" + sender_uniqueProposal_ID + "," + sender_proposal_Val + ") <------------ M" + sender_Member_ID);
                }
//                if(number_Of_promises_Received.size() == (((max_num_Member-1)/2) + 1)) {
//                    if (sender_bool_accepted_Val == true) {
//                        this.proposal_Val = sender_accepted_proposal_Val;
//                    }
//                    message propose_Msg = new message("Propose Msg", this.member_ID, sender_uniqueProposal_ID, sender_acceptedUnique_Proposal_ID, this.proposal_Val, this.bool_accepted_val);
//                    sendToAll(propose_Msg, false);
//                }
//                else if(number_Of_promises_Received.size() < (((max_num_Member-1)/2) + 1)){
//                    System.out.println("[Phase 2(a)] : M" + this.member_ID + " receives less than half of the Promises. So it will resend with a new Prepare Msg.");
//                    prepare();
//                }
            }

            /*
                Phase 2(b): This is where members will receive Propose Msg from the Proposers
                1. The members will check to see if its own max_Proposal_ID == the proposal_ID from the Propose() Msg
                    a. If yes, set its bool_accepted_val = true,
                               set its accepted_Proposal_ID = the proposal_ID from the Propose() Msg
                               set its accepted_Proposal_Val = the proposal_Val from the Propose() Msg
                               send back an Accepted(accepted_Proposal_ID, accepted_Proposal_Val) Msg to the corresponding Proposers.
                    b. If no, simply ignore the messages.
             */
            else if(MsgObj_From.getMessage_Type().equals("Propose Msg")){
                int sender_Member_ID = MsgObj_From.getSender_Member_ID();
                double sender_uniqueProposal_ID = MsgObj_From.getUnique_proposal_ID();
                double sender_acceptedUnique_Proposal_ID = MsgObj_From.getAccepted_unique_Proposal_ID();
                int sender_proposal_Val = MsgObj_From.getProposal_Value();
//                if(this.is_Offline == true){
//                    prepare();
//                }

                if(sender_uniqueProposal_ID == this.max_Proposal_ID && is_Offline == false){
                    this.bool_accepted_val = true;
                    this.accepted_proposal_ID = sender_uniqueProposal_ID;
                    this.accepted_proposal_Val = sender_proposal_Val;
                    System.out.println("[Phase 2(b)] : M" + this.member_ID + " sends Accepted(" + sender_uniqueProposal_ID + "," + sender_proposal_Val + ") ------------> M" + sender_Member_ID);
                    message accepted_Msg = new message("Accepted Msg", this.member_ID, sender_uniqueProposal_ID, sender_acceptedUnique_Proposal_ID, sender_proposal_Val, this.bool_accepted_val);
                    send(sender_Member_ID, accepted_Msg);

                }else if(sender_uniqueProposal_ID == this.max_Proposal_ID && is_Offline){
                    // Ignore
                    System.out.println("M" + this.member_ID + " is offline.");
                }
                else if(sender_uniqueProposal_ID != this.max_Proposal_ID){
                    // Ignore
                }
            }

            /*
                Phase 3(a): Proposers (M1-M3) receive Accepted(accepted_proposal_ID, accepted_proposal_Val) Msg from the members that accepted its proposal in Phase 2(b).
                1. The proposer will check to see if the number of Accepted() msg exceeds the majority of members
                    a. If yes, send a final message called last_Confirmed_Msg(accepted_proposal_ID, accepted_proposal_Val) to all members including itself. (bool_BroadCast = true)
                    b. If no, simply ignore the messages.
             */
            else if(MsgObj_From.getMessage_Type().equals("Accepted Msg")){
                int sender_Member_ID = MsgObj_From.getSender_Member_ID();
                double sender_uniqueProposal_ID = MsgObj_From.getUnique_proposal_ID();
                double sender_acceptedUnique_Proposal_ID = MsgObj_From.getAccepted_unique_Proposal_ID();
                int sender_proposal_Val = MsgObj_From.getProposal_Value();
                boolean sender_bool_accepted_Val = MsgObj_From.getProposal_Accepted();

                number_Of_accepted_Received.add(MsgObj_From);
                System.out.println("[Phase 3(a)] : M" + this.member_ID + " receives Accepted(" + sender_uniqueProposal_ID + "," + sender_proposal_Val + ") [" + number_Of_accepted_Received.size() + " time]" + "<------------ M" + sender_Member_ID);
                if(number_Of_accepted_Received.size() == (((max_num_Member-1)/2)+1)){
                    message last_confirmed_Msg = new message("Last Confirmed Msg", this.member_ID, sender_uniqueProposal_ID, sender_acceptedUnique_Proposal_ID, sender_proposal_Val, sender_bool_accepted_Val);
                    number_Of_promises_Received.clear();
                    number_Of_accepted_Received.clear();
                    sendToAll(last_confirmed_Msg, true);
                }
            }

            /*
                Phase 3(b): This is where all members will receive the final message confirming the consensus on the final proposal val.
             */
            else if(MsgObj_From.getMessage_Type().equals("Last Confirmed Msg")){
                int sender_Member_ID = MsgObj_From.getSender_Member_ID();
                double final_acceptedUnique_Proposal_ID = MsgObj_From.getAccepted_unique_Proposal_ID();
                double final_uniqueProposal_ID = MsgObj_From.getUnique_proposal_ID();
                int final_Proposal_Val = MsgObj_From.getProposal_Value();

                this.final_Max_Proposal_ID = final_uniqueProposal_ID;
                this.last_accepted_Proposal_ID = final_acceptedUnique_Proposal_ID;
                this.final_Proposal_Val = final_Proposal_Val;

                System.out.println("[Phase 3(b)] : M"+ this.member_ID + " final accepted proposal is Propose(" + final_uniqueProposal_ID + "," + final_acceptedUnique_Proposal_ID + "," + final_Proposal_Val + ") <------------ M" + sender_Member_ID);

                bool_Consensus = true;
            }

            // This is where the failed prepare messages get to, if a proposer receives half+1 failed messages, it will resend the failed prepare messages with a higher unique_proposal_ID
            else if(MsgObj_From.getMessage_Type().equals("Resend Prepare")){
                number_Of_Fail_Prepare.add(MsgObj_From);
                if(number_Of_Fail_Prepare.size() == (((max_num_Member-1)/2) + 1)){
                    number_Of_Fail_Prepare.clear();
                    prepare();
                }
            }
            read_from.close();

        }catch(Exception e){
            System.err.println("Error in reading from M" + this.member_ID + " ObjectOutputStream !!");
        }
    }

    public int getMembersID(){
        return member_ID;
    }
}