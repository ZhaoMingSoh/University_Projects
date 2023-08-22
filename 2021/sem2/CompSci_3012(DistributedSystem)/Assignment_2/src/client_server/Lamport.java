package client_server;

public class Lamport {
    private int lamport_1;
    private int lamport_2;

    public Lamport(int lamport_1, int lamport_2){
        this.lamport_1 = lamport_1;
        this.lamport_2 = lamport_2;
    }

    public int get_Lamport(){
        int larger_lamport = 0;
        if(lamport_1 >= lamport_2){
            larger_lamport = lamport_1++;
        }else{
            larger_lamport = lamport_2++;
        }
        return larger_lamport;
    }
}
