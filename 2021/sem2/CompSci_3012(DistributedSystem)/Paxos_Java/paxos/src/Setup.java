import java.util.ArrayList;

public class Setup {
    ArrayList<Members> all_Members = new ArrayList<>();

    public void Member_Creation(String[] response_Times){
        all_Members.add(new Members(1, GlobalVariable.base_port + (1 * 100), "Proposer", ""));
        all_Members.add(new Members(2, GlobalVariable.base_port + (2 * 100), "Proposer", ""));
        all_Members.add(new Members(3, GlobalVariable.base_port + (3 * 100), "Proposer", ""));
        all_Members.add(new Members(4, GlobalVariable.base_port + (4 * 100), "Acceptor", response_Times[0]));
        all_Members.add(new Members(5, GlobalVariable.base_port + (5 * 100), "Acceptor", response_Times[1]));
        all_Members.add(new Members(6, GlobalVariable.base_port + (6 * 100), "Acceptor", response_Times[2]));
        all_Members.add(new Members(7, GlobalVariable.base_port + (7 * 100), "Acceptor", response_Times[3]));
        all_Members.add(new Members(8, GlobalVariable.base_port + (8 * 100), "Acceptor", response_Times[4]));
        all_Members.add(new Members(9, GlobalVariable.base_port + (9 * 100), "Acceptor", response_Times[5]));

        synchronized (this){
            for(int i=0; i<all_Members.size(); i++){
                Instantiate_Threads create_MembersServerSocket = new Instantiate_Threads(all_Members.get(i));
                create_MembersServerSocket.start();
            }
        }
    }

    public void start_Prepare(int proposer_ID, String delayType, boolean is_Offline){
        for(int i=0; i<all_Members.size(); i++){
            if(all_Members.get(i).id == proposer_ID) {
                all_Members.get(i).delay_type = delayType;
                start_Prepare_Threads startProposerThreads = new start_Prepare_Threads(all_Members.get(i));
                startProposerThreads.start();
            }
        }
    }

    public static class Instantiate_Threads extends Thread{
        Members temp;

        public Instantiate_Threads(Members temp){
            this.temp = temp;
        }

        public void run(){
            temp.connect_members();
        }
    }

    public static class start_Prepare_Threads extends Thread{
        Members proposer;

        public start_Prepare_Threads(Members proposer){
            this.proposer = proposer;
        }

        public void run(){
            proposer.prepare();
        }
    }
}
