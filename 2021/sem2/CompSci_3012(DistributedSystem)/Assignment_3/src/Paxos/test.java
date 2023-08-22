package Paxos;

public class test {
    public static void main(String[] args) {
        int[] a = {1,2,3,4,5,6};
        for(int k : a){
            System.out.println(k);
        }

        double p_id = 0;
        String decimal = String.valueOf(1) + "." + String.valueOf(1);
        p_id = Double.valueOf(decimal);

        System.out.println(p_id++);
    }
}
