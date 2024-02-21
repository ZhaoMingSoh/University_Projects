package paxos;

import java.util.ArrayList;

public class setup {
    ArrayList<members> all_Members = new ArrayList<>();
    final static int port_Num = 6060;

    public void Member_Creation(int num_Members, String[] response_Times){
        all_Members.add(new members(1, port_Num + (1 * 100), num_Members, "Proposer", ""));
        all_Members.add(new members(2, port_Num + (2 * 100), num_Members, "Proposer", ""));
        all_Members.add(new members(3, port_Num + (3 * 100), num_Members, "Proposer", ""));
        all_Members.add(new members(4, port_Num + (4 * 100), num_Members, "Acceptor", response_Times[0]));
        all_Members.add(new members(5, port_Num + (5 * 100), num_Members, "Acceptor", response_Times[1]));
        all_Members.add(new members(6, port_Num + (6 * 100), num_Members, "Acceptor", response_Times[2]));
        all_Members.add(new members(7, port_Num + (7 * 100), num_Members, "Acceptor", response_Times[3]));
        all_Members.add(new members(8, port_Num + (8 * 100), num_Members, "Acceptor", response_Times[4]));
        all_Members.add(new members(9, port_Num + (9 * 100), num_Members, "Acceptor", response_Times[5]));

        synchronized (this){
            for(int i=0; i<all_Members.size(); i++){
                Instantiate_Threads create_MembersServerSocket = new Instantiate_Threads(all_Members.get(i));
                create_MembersServerSocket.start();
            }
        }
    }

    public void start_Prepare(int proposer_ID, String delayType, boolean is_Offline){
        for(int i=0; i<all_Members.size(); i++){
            if(all_Members.get(i).getMembersID() == proposer_ID) {
                all_Members.get(i).delay_Type = delayType;
                all_Members.get(i).is_Offline = is_Offline;
                start_Prepare_Threads startProposerThreads = new start_Prepare_Threads(all_Members.get(i));
                startProposerThreads.start();
            }
        }
    }

    public static class Instantiate_Threads extends Thread{
        members temp;

        public Instantiate_Threads(members temp){
            this.temp = temp;
        }

        public void run(){
            temp.connect_To_Other_Members();
        }
    }

    public static class start_Prepare_Threads extends Thread{
        members proposer;

        public start_Prepare_Threads(members proposer){
            this.proposer = proposer;
        }

        public void run(){
            proposer.prepare();
        }
    }
}
