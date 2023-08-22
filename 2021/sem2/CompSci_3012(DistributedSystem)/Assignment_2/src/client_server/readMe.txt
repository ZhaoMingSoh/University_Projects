Key in the following to run the program:
1. bash compile.sh // compile all the relevant java files and run the Atom_Server
2. bash content_server.sh // run the Content_Servers (1 to 5)
3. bash client.sh // run the Client (1 to 5)

Brief Explanation of how the program works:
1. When the Atom_Server is started, it will wait for either a Content_Server or a Client to request for connection.
2. When the Content_Server is started, it will convert the given input_(1-5).txt file into Atom Feed XML document at which it
   will perform a PUT operation that sends the Atom Feed XML document to the Atom_Server.
4. Once the Atom_Server receives the PUT message from the Content_Server, it will combine the given Atom Feed XML document
   to an aggregate.xml file. Upon finishing the aggregation of the Atom Feed XML document, it will send a response back to
   the Content_Server.
3. When the Client is started, it will send a GET request to the Atom_Server.
5. Once the Atom_Server receives the GET message from the Client, it will then send the aggregate.xml file over to the Client
   as a response.

Things that I haven't done:
1. Error checking for the validity and presence of the Atom Feed Key Elements in the input_(1-5).txt files.
3. Error checking for messages.
2. Both of my Content_Servers and Client are yet to be able to sustain a persistent connection with the Atom_Server.
   Because of this I am not able to do Lamport Clock and Heartbeat algorithms.

Some questions that I would like to clarify on:
1. They way that my Atom_Server handles multiple Client/Content_Server requests is by spawning new threads. Should I keep
   track of the threads in order to simulate the Lamport behaviour ?
2. Since, socket programming automatically orders the processing of the requests, why do we still need Lamport clock ?