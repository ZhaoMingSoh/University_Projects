#!/bin/bash
javac *.java
cd ../
java paxos.test ./paxos/Testing/Test_1/Resulting_Output.txt ./paxos/Testing/Test_1/Expected_Output.txt Test1
