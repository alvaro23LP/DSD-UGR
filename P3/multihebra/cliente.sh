echo "Lanzando cliente con 6 hebras"
echo
java -cp . -Djava.security.policy=server.policy Cliente_Ejemplo_Multi_Threaded localhost 6
sleep 1
