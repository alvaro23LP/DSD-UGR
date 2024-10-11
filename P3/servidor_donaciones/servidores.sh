#!/bin/sh -e
echo "Compilando archivos .java"
javac *.java 
sleep 1
echo
echo "Lanzando servidores"
java -cp . -Djava.rmi.server.codebase=file:./ -Djava.rmi.server.hostname=localhost -Djava.security.policy=server.policy Servidor $1
