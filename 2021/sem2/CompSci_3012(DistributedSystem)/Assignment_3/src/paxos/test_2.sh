#!/bin/bash
javac *.java
cd ../
java paxos.test ./paxos/Testing/Test_2/Resulting_Output.txt ./paxos/Testing/Test_2/Expected_Output.txt Test2