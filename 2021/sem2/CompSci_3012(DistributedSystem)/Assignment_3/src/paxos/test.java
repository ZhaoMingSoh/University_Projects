package paxos;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

public class test {
    static String test_file_Path = "";
    static String expected_Output_File_Path = "";
    public static void main(String[] args) {
        try {
            test_file_Path = args[0];
            expected_Output_File_Path = args[1];
            File test = new File(args[0]);
            File expected_Output = new File(args[1]);
            if (test.exists()) {
                BufferedWriter writer = new BufferedWriter(new FileWriter(test));
                writer.write("");
                writer.close();
            }else{
                System.out.println("Error: File at " + args[0] + " does not exist.");
            }
            if(expected_Output.exists()){
                BufferedWriter writer = new BufferedWriter(new FileWriter(expected_Output));
                writer.write("");
                writer.close();
            }else{
                System.out.println("Error: File at " + args[1] + " does not exist.");
            }
        } catch (IOException e) {
            System.err.println("Error : Unable to open " + args[0] + " or " + args[1]);
            e.printStackTrace();
        }

        // Every compilation and running of the Test executable will clear out the Resulting_Output.txt in Test_1
        if(args[2].equals("Test1")) {
            System.out.println("[Test 1: M1-M3 sends prepare messages at the same time to every other members excluding itself.\n"+
                    "          The members that received the prepare messages have immediate response times.]");
            System.out.println();
            setup test_1 = new setup();
            String[] response_times = new String[6];
            Arrays.fill(response_times, "immediate");
            test_1.Member_Creation(9, response_times);
            test_1.start_Prepare(1, "immediate", false);
            test_1.start_Prepare(2, "immediate", false);
            test_1.start_Prepare(3, "immediate", false);

        }else if(args[2].equals("Test2")){
            System.out.println("[Test 2: M1-M9 have different response times such as 'Immediate', 'late', 'medium' but do not have 'never']");
            System.out.println();
            setup test_1 = new setup();
            String[] response_times = {"immediate", "medium", "late", "medium", "immediate", "late"};
            test_1.Member_Creation(9, response_times);
            test_1.start_Prepare(1, "immediate", false);
            test_1.start_Prepare(2, "late", false);
            test_1.start_Prepare(3, "medium", false);

        }else if(args[2].equals("Test3")){
            System.out.println("[Test 3: M1-M9 have different response times such as 'Immediate', 'late', 'medium' but do not have 'never' " +
                    "and M2 and M3 will be disconnected once they sent their Propose Msg. ]");
            System.out.println();
            setup test_1 = new setup();
            String[] response_times = {"late", "medium", "immediate", "medium", "late", "immediate"};
            test_1.Member_Creation(9, response_times);
            test_1.start_Prepare(1, "immediate", false);
            test_1.start_Prepare(2, "late", true);
            test_1.start_Prepare(3, "medium", true);

        }else if(args[2].equals("Test4")){
            System.out.println("[Test 4: M1-M3 have different response times such as 'Immediate', 'late', 'medium', 'never' " +
                    "and M2 and M3 will be disconnected once they sent their Propose Msg ]");
            System.out.println();
            setup test_1 = new setup();
            String[] response_times = {"never", "never", "immediate", "medium", "medium", "late"};
            test_1.Member_Creation(9, response_times);
            test_1.start_Prepare(1, "immediate", false);
            test_1.start_Prepare(2, "late", false);
            test_1.start_Prepare(3, "medium", false);

        }
    }
}