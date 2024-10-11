javac *.java
echo
echo "Lanzando cliente"
java -cp . -Djava.security.policy=server.policy Cliente $1
