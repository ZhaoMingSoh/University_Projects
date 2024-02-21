Explanation of How my basic paxos program works:

1. Starting off in the test.java file, call the member_Creation(n) in the setup.java file --->
   which will create 'n' number of members' object and store them in an Array. Then loop through the array to assign a
   different thread for each of member object. Then in the members.java file, create a ServerSocket for each of the
   member each at different port numbers. Once, each member has been initialised as a ServerSocket, they will listen
   for any incoming socket connections from each other.

2. Again, in the test.java file, called the start_Prepare(proposer ID) for M1, M2 and M3 in the setup.java file --->
   this will