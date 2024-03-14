import socket
import threading
import math

# Configuration
# Proposers
NUM_PMEMBERS = 3
PMEMBERS_ID = [i for i in range(1,NUM_PMEMBERS+1)]
PPORTS = [5000 + i for i in range(1,NUM_PMEMBERS+1)]
# Acceptors/Learners
NUM_MEMBERS = 6
MEMBERS_ID = [i for i in range(4,NUM_PMEMBERS+NUM_MEMBERS+1)] 
PORTS = [5000 + i for i in range(4,NUM_PMEMBERS+NUM_MEMBERS+1)]

MAJORITY = math.ceil((NUM_PMEMBERS+NUM_MEMBERS)/2)
ALL_PORTS = [5000 + i for i in range(1, NUM_PMEMBERS+NUM_MEMBERS+1)]

# Message types
PREPARE = "PREPARE"
PROMISE = "PROMISE"
ACCEPT_REQUEST = "ACCEPT_REQUEST"
ACCEPT = "ACCEPT"
ACCEPTED = "ACCEPTED"

class PaxosNode :
    def __init__(self, id, port, value = None) -> None:
        self.id = id
        self.port = port
        # proposer value
        self.proposal_value = value # if None means it is an acceptor/learner
        # proposal_id : the id it got from prepare, promise, accept-request & accept messages
        # highest_proposal_id : the highest id it got so far from proposal_id
        self.temp_id = 0
        self.proposal_id = 0.0  # use decimal to create unique proposal ID for every paxos node
        self.highest_proposal_id = 0
        # accepted_value : value in which consensus has been reached
        # accepted_id : id in which the consensus is reached
        self.accepted_value = None
        self.highest_accepted_id = 0
        self.promises = []
        self.accept = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("localhost", port))
        self.start_listener()
    
    def start_listener(self):
        listener = threading.Thread(target=self.listen, args=())
        listener.start()

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024) # from which paxos node the data & address is from
            data = data.decode()
            message_type, proposal_id, value_id, value, source = data.split("|") # the data has the phases' messages content and the source paxos node id
            proposal_id = float(proposal_id)
            if value_id == "":
                value_id = 0.0
            else:
                value_id = float(value_id)
            
            if message_type== PREPARE:
                print(f"Prepare(recv) : M{self.id} <---- PREPARE[{proposal_id}] from M{source}")
                self.handle_prepare(addr, proposal_id)
            elif message_type == PROMISE:
                print(f"Promise(recv) : M{self.id} <------ PROMISE[{proposal_id},{value_id},{value}] from M{source}")
                self.handle_promise(addr, proposal_id, value_id, value, source)   
            elif message_type == ACCEPT_REQUEST:
                print(f"Accept_request(recv) : M{self.id} <---------- ACCEPT_REQUEST[{max(proposal_id, value_id)},{value}] from M{source}")
                self.handle_accept_request(addr, max(proposal_id, value_id), value)
            elif message_type == ACCEPT:
                print(f"Accept(recv) : M{self.id} <------------ ACCEPT[{proposal_id},{value}] from M{source}")
                self.handle_accepted(proposal_id, value, source)
            elif message_type == ACCEPTED:
                print(f"Accepted(recv) : M{self.id} <------------ ACCEPTED[{proposal_id},{value}] from M{source}")
                print(f"{self.id } : {value} is the new President of the council!")

    """
    2) members accept prepare messages for a particular proposal_id
        - compare the current paxos node's highest_proposal_id to the newly received proposal_id
            if proposal_id < highest_proposal_id :
                Ignore
            if proposal_id > highest_proposal_id :
                - if it has already accepted a value, send PROMISE[proposal_id, accepted_id, accepted_value]
                - if not, send PROMISE[proposal_id]
    """
    def handle_prepare(self, addr, proposal_id):
        if proposal_id > self.highest_proposal_id:
            self.highest_proposal_id = proposal_id
            promise_message = None
            if self.accepted_value is not None:
                promise_message = f"{PROMISE}|{proposal_id}|{self.highest_accepted_id}|{self.accepted_value}|{self.id}"
            else:
                promise_message = f"{PROMISE}|{proposal_id}|||{self.id}"
            self.send_message(addr, promise_message)
        else:
            print("(Ignore)")

    """
    3) proposer gets a majority of promise messages for a specific proposal_id :
        - checks if is has got any accepted value from promises :
            - if yes, sends ACCEPT_REQUEST[proposal_id, proposal_id, value]
            - if no, sends ACCEPT_REQUEST[highest_proposal_id, value]
    """
    def handle_promise(self, addr, proposal_id, value_id, value, source):
        self.promises.append({addr,value_id,value,source})
        if len(self.promises) >= MAJORITY:
            accept_request_message = None
            if value:
                accept_request_message = f"{ACCEPT_REQUEST}|{proposal_id}|{max(value_id, proposal_id)}|{value}|{self.id}"
            else:
                accept_request_message = f"{ACCEPT_REQUEST}|{proposal_id}||{self.proposal_value}|{self.id}"
            self.broadcast(accept_request_message)
    
    """
    4) members receive the accept_request messages for a specific proposal_id :
        - compare the current paxos node's highest_accepted_id to the newly received proposal_id
        -   if proposal_id > highest_accepted_id
            - sends ACCEPT[proposal_id, value]
    """
    def handle_accept_request(self, addr, proposal_id, value):
        if proposal_id > self.highest_accepted_id:
            accept_message = f"{ACCEPT}|{proposal_id}||{value}|{self.id}"
            self.send_message(addr, accept_message)
    
    """
    5) proposer receives the accept messages for a specific id & value :
        - if there is majority accept messages received, this mean that a consensus has been reached.
    """
    def handle_accepted(self, proposal_id, value, source):
        self.accept.append({self.id, proposal_id, value, source})
        if len(self.accept) > MAJORITY:
            self.accepted_value = value
            self.highest_accepted_id = proposal_id
            accepted_message = f"{ACCEPTED}|{proposal_id}||{value}|{self.id}"
            self.broadcast(accepted_message)
    
    def send_message(self, addr, message):
        self.sock.sendto(message.encode(), addr)

    def broadcast(self, message):
        message_type,proposal_id,value_id,value,source = message.split("|")
        # printout of broadcasted messages must be here (not in send_message) to avoid duplicate printouts, cause a single node can send the same message to multiple other nodes.
        if message_type == PREPARE:
            print(f"\nM{source} --> PREPARE[{proposal_id}] to everyone\n")
        elif message_type == ACCEPT_REQUEST:
            print(f"\nAccept_request[OUT] : M{source} --------> ACCEPT_REQUEST[{proposal_id},{value}] to everyone\n")
        elif message_type == ACCEPT:
            print(f"\nAccept[OUT] : M{source} ----------> ACCEPT[{proposal_id},{value}] to everyone\n")
        elif message_type == ACCEPTED:
            print(f"\nAccepted[OUT] : M{source} ----------> ACCEPTED[{proposal_id},{value}] to everyone\n")
        for port in ALL_PORTS:
            if port != self.port:
                self.send_message(("localhost", port), message)
    
    """
    1) proposer sends prepare messages to every other paxos nodes except itself.
    """
    def propose(self):
        self.temp_id += 1
        self.proposal_id = self.temp_id + self.id/10
        prepare_message = f"{PREPARE}|{self.proposal_id}|||{self.id}"
        self.broadcast(prepare_message)


if __name__ == "__main__":
    # Initialise and create the paxos nodes
    proposer_nodes = [PaxosNode(id, port, value) for id, port, value in zip(PMEMBERS_ID,PPORTS,PMEMBERS_ID)]
    paxos_nodes = [PaxosNode(id, port) for id, port in zip(MEMBERS_ID,PORTS)]

    # Initiate the paxos algorithm
    for p_node in proposer_nodes:
        p_node.propose()
