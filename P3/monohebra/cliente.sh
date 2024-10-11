
echo "Lanzando cliente 0"
echo
java -cp . -Djava.security.policy=server.policy Cliente_Ejemplo localhost 0
sleep 1
echo "Lanzando cliente 1"
echo
java -cp . -Djava.security.policy=server.policy Cliente_Ejemplo localhost 1
sleep 1
