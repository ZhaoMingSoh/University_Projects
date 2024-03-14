from paxosNodes import PaxosNode

import threading

NODES = 9
PROPOSERS = 3
ACCEPTORS = 6
BASE_PORT = 6000
PORTS = [BASE_PORT + (node_id * 100) for node_id in range(1,NODES+1)]

if __name__ == "__main__":
    # Test 1 : No delays, disconnections
    proposers = [PaxosNode("Proposer", i, BASE_PORT + (i*100), i, "immediate") for i in range(1,PROPOSERS+1)]
    acceptors = [PaxosNode("Acceptor", i, BASE_PORT + (i*100), i, "immediate") for i in range(4,PROPOSERS+ACCEPTORS+1)]

    for acceptor in acceptors:
        acceptor_thread = threading.Thread(target=acceptor.handle_connection)
        acceptor_thread.start()
    
    for proposer in proposers:
        proposer_thread = threading.Thread(target=proposer.handle_connection)
        proposer_thread.start()

    for proposer in proposers:
        proposer.prepare()