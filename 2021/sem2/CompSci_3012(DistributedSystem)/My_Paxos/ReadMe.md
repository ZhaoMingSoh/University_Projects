# Paxos Algorithm

## Characteristics :

1. A majority of the servers must be up for Paxos to terminate or reach concensus. Need 2m+1 servers to tolerate m failures.
2. Failure Model :
   - Slow propagation of messages
   - Network failure
   - Node failure (fail stop) where it completely stops sending any messages

### Steps :

![alt text](<Screenshot 2024-03-07 at 8.03.22 PM.png>)

I fail to implement the paxos algorithm because I am having trouble understanding how to create a working multi servers and clients architecture to simulate the communications.

- I tried to do somehting similar to what was done in Java, creating individual threads to handle each of the members server socket, and then using individual threads to start the paxos algorithm, and then using the port num of each members to send messages to the correct server socket or using the accepted client-socket to send messages back. For some reasons, python doesn't allow the latter.
  - server sockets for each members are created as such :
    ```python
      self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # ------- and -------
      client_socket, addr = self.server_sock.accept()
      # ....
      seriliased_msg = client_socket.recv(1024)
      # ....
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
    ```
