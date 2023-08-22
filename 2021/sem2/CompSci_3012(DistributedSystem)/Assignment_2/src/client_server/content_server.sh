#!/bin/bash
clear
echo "Starting Content Server 1 ......"
cd ..
java -cp ".:./jars/*" client_server.Content_Server localhost:9090 ./client_server/resources/input_1.txt
sleep 1
echo "Starting Content Server 2 ......"
java -cp ".:./jars/*" client_server.Content_Server localhost:9090 ./client_server/resources/input_2.txt
sleep 1
echo "Starting Content Server 3 ......"
java -cp ".:./jars/*" client_server.Content_Server localhost:9090 ./client_server/resources/input_3.txt
sleep 1
echo "Starting Content Server 4 ......"
java -cp ".:./jars/*" client_server.Content_Server localhost:9090 ./client_server/resources/input_4.txt
echo "Starting Content Server 5 ......"
java -cp ".:./jars/*" client_server.Content_Server localhost:9090 ./client_server/resources/input_5.txt