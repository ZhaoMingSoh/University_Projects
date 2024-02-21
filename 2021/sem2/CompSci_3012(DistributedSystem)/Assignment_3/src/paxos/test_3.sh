#!/bin/bash
javac *.java
cd ../
java paxos.test ./paxos/Testing/Test_3/Resulting_Output.txt ./paxos/Testing/Test_3/Expected_Output.txt Test3