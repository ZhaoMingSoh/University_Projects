# Paxos Algorithm designed to simulate a suburbs council election for a president

- As for nitty-griddy details of the algoritm, refer to these links

  - https://segmentfault.com/a/1190000040849250
  - https://people.cs.rutgers.edu/~pxk/417/notes/paxos.html

- They way I approach the implementation :

  - Create a server socket for each members on individual threads
  - Use individual threads to start the prepare phase of the algorithm
  - send messages in the prepare, promise and accept by opening up sockets using members' id

- My implementation focuses on members assuming the role of proposers and acceptors, meaning messages strictly get transferred in this order :

  - Proposers send Prepare(ID) message to every Acceptors/including other Proposers.
  - Acceptors receive Prepare(ID) message and send Promise(ID,Accept ID,Accept Val) to Proposers.
  - Proposers send Propose(ID,Val) message to every Acceptors/including other Proposers.
  - Acceptors receive Propose(ID,Val) message and send Accept(ID,Val) to Proposers.
  - Proposers receive Accept(ID,Val) message and send Final(ID,Val) to every Acceptors/including other Proposers.

- A lot of edge cases and network erros are kinda hard to simulate :

  - When proposers/acceptors timeouts during each of the phases. How to implement ?
  - Byzantile faults ? How to make proposers/acceptors be malicious ?

- The only things I did was :
  - The paxos algorithm in different timeouts during the sending of the messages.
