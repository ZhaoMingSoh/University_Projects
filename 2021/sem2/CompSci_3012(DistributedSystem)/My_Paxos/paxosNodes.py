import socket
from decimal import Decimal
from message import message
import threading
import pickle # for serialising and deserialising python objects
import math

NODES = 9
MAJORITY = math.ceil(NODES/2)
BASE_PORT = 6000
PORTS = [BASE_PORT + (node_id * 100) for node_id in range(1,NODES+1)]

class PaxosNode:
    # socket connections attributes
    server_sock = None
    bool_consensus = False
    server_thread = None
    promises = None

    # proposer attributes
    temp_id = 0
    proposal_id = 0.0
    bool_accepted_proposal = False
    accepted_id = 0.0
    accepted_val = None

    # acceptor attributes
    max_id = 0.0

    def __init__(self, node_type, id, port_num, proposal_val, delay_type) -> None:
        self.node_type = node_type
        self.id = id
        self.port_num = port_num
        self.proposal_val = proposal_val
        self.delay_type = delay_type
        # Create a server socket for each node
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("localhost", port_num))
        print(f'Node M{id} started as a server on port {port_num}')

    def handle_connection(self):
        self.server_sock.listen()
        try:
            while self.bool_consensus == False:
                client_socket, addr = self.server_sock.accept()
                connection_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr,))
                connection_thread.start()
        except Exception as e:
            print(f'[Threading Error] : Problem with the connection thread for node M{self.id}')
            print(e)
     
    def handle_client(self, client_socket, addr):
        try:
            seriliased_msg = client_socket.recv(1024)
            # decode the serialised message object
            client_data = pickle.loads(seriliased_msg)
            print(client_data.message_type)
    
            """
                Phase 1b :
                    acceptors receive the prepare(proposal_id) from proposers
                    if (ID <= max_id)
                        do not respond (or respond with a "fail" message)
                    else
                        max_id = ID     // save highest ID we've seen so far
                        if (proposal_accepted == true) // was a proposal already accepted?
                            respond: PROMISE(ID, accepted_ID, accepted_VALUE)
                        else
                            respond: PROMISE(ID)
            """
            if client_data.message_type == "prepare":
                id = client_data.proposal_id
                source_id = client_data.source_id

                if id <= self.max_id:
                    print(f"[Phase 1b] : Fails as the proposal id from M{source_id} : {id} < M{self.id} : {self.max_id}")
                else:
                    self.max_id = id
                    promise_msg = None
                    if self.bool_accepted_proposal:
                        accepted_id = self.accepted_id
                        accepted_val = self.accepted_val
                        promise_msg = message("promise", self.id, id, None, accepted_id, accepted_val, self.bool_accepted_proposal)
                    else:
                        promise_msg = message("promise", self.id, id, None, 0.0, None, self.bool_accepted_proposal)
                    client_socket.send(pickle.dumps(promise_msg))
                """
                    Phase 2a :
                    did I receive PROMISE responses from a majority of acceptors?
                    if yes
                        do any responses contain accepted values (from other proposals)?
                        if yes
                            val = accepted_VALUE    // value from PROMISE message with the highest accepted ID
                        if no
                            val = VALUE     // we can use our proposed value
                        send PROPOSE(ID, val) to at least a majority of acceptors
                """
            elif client_data.message_type == "promise":
                self.promises.append(client_data)
                if len(self.promises) < MAJORITY:
                    print(f"[Phase 1b] : Fails on M{self.id}, no majority of promises.")
                else:
                    id = client_data.proposal_id
                    bool_accepted_proposal = client_data.bool_accepted_proposal
                    highest_id = -1.0
                    highest_id_val = None
                    propose_msg = None

                    if bool_accepted_proposal:
                        for promise in self.promises:
                            if promise.accepted_proposal_id > highest_id:
                                highest_id = promise.accepted_proposal_id
                                highest_id_val = promise.accepted_proposal_val
                        if id > highest_id:
                            highest_id = id
                        propose_msg = message("propose", self.id, id, None, highest_id, highest_id_val, bool_accepted_proposal)
                    else:
                        propose_msg = message("propose", self.id, id, self.proposal_val, 0.0, None, bool_accepted_proposal)
                    
                    self.broadcast(propose_msg)
                """
                    if (ID == max_id) // is the ID the largest I have seen so far?
                        proposal_accepted = true     // note that we accepted a proposal
                        accepted_ID = ID             // save the accepted proposal number
                        accepted_VALUE = VALUE       // save the accepted proposal data
                        respond: ACCEPTED(ID, VALUE) to the proposer and all learners
                    else
                        do not respond (or respond with a "fail" message)
                """
            elif client_data.message_type == "propose":
                print("hey")
                            
        except Exception as e:
            print(f"[Handling Client Error] : Problem with node M{self.id} accepting client connection.")
            print(e)

    """
        Phase 1a:
            proposers send Prepare(proposal_id) to every other nodes except themselves.
    """
    def prepare(self):
        self.temp_id += 1
        self.proposal_id = Decimal(str(self.temp_id) + '.' + str(self.id))
        prepare_msg = message("prepare", self.id, self.proposal_id, None, 0.0, None, False)
        self.broadcast(prepare_msg)
    
    def broadcast(self, message):
        if message.message_type == "prepare":
            print(f'[Phase 1a] M{message.source_id} ------> Prepare({self.proposal_id})')
        elif message.message_type == "propose":
            print(f"[Phase 2a] M{message.source_id} ------> Propose({message})")
        for port in PORTS:
            if port != self.port_num:
                client_addr = ('localhost', port)
                self.send_message(client_addr, message)

    def send_message(self, client_addr, message):
        serialised_msg = pickle.dumps(message)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
                client_sock.connect(client_addr)
                client_sock.sendall(serialised_msg)
        except Exception as e:
            print(f"[Sending Error] : Problem with node M{self.id} sending message.")
            print(e)
    
    # send messages back to the proposer using the client_socket from the acc
    # def send_message_back(self, client_socket, message):
    #     if message.message_type == "promise":
    #         print(f'[Phase 1b] M{message.source_id} ------> Promise({message.proposal_id},{message.accepted_proposal_id},{message.accepted_proposal_val})')

    #     serialised_msg = pickle.dumps(message)
    #     # Get the proposer's address from the client socket
    #     proposer_addr = client_socket.getpeername()

    #     try:
    #         # Create a new client socket and connect to the proposer
    #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
    #             client_sock.connect(proposer_addr)
    #             client_sock.sendall(serialised_msg)
    #     except Exception as e:
    #         print(f"[Sending Error] : Problem with node M{self.id} sending message back to the proposer.")
    #         print(e)
