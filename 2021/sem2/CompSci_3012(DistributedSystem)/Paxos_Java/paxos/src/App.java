import java.util.Arrays;

public class App {
    public static void main(String[] args) throws Exception {
        // Test 1 - no delays or disconnections
        // Setup test1 = new Setup();
        // String[] response_times = new String[6];
        // Arrays.fill(response_times, "immediate");
        // test1.Member_Creation(response_times);
        // test1.start_Prepare(1, "immediate", false);
        // test1.start_Prepare(2, "immediate", false);
        // test1.start_Prepare(3, "immediate", false);

        // Test 2 - varying levels of delays, no disconnections
        Setup test2 = new Setup();
        String[] response_times = {"immediate", "immediate", "late", "medium", "medium", "late"};
        test2.Member_Creation(response_times);
        test2.start_Prepare(1, "medium", false);
        test2.start_Prepare(2, "immediate", false);
        test2.start_Prepare(3, "late", false);
    }
}
