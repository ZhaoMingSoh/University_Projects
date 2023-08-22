#!/bin/bash
clear
echo "Starting Content Client 1 ......"
cd ..
java -cp ".:./jars/*" client_server.Client localhost:9090
sleep 1
echo "Starting Content Client 2 ......"
java -cp ".:./jars/*" client_server.Client localhost:9090
sleep 1
echo "Starting Content Client 3 ......"
java -cp ".:./jars/*" client_server.Client localhost:9090
sleep 1
echo "Starting Content Client 4 ......"
java -cp ".:./jars/*" client_server.Client localhost:9090
sleep 1
echo "Starting Content Client 5 ......"
java -cp ".:./jars/*" client_server.Client localhost:9090