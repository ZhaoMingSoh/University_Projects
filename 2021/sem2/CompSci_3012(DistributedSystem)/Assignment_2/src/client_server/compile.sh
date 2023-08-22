#!/bin/bash
clear
echo "Compiling files ......"
cd ..
javac -cp ".:./jars/*" client_server/*.java
echo "Finished Compiling"
echo "Starting Atom Server ......"
java -cp ".:./jars/*" client_server.Atom_Server
echo "Atom Server has started"