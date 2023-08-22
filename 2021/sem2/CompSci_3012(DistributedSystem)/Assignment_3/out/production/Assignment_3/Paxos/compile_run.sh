#!/bin/bash
echo "Compiling ......"
javac Members.java Messages.java Paxos.java
echo "Finished Compiling ......"
cd ../
echo "Starting Paxos Server ......"
java Paxos.Paxos
