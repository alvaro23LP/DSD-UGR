
echo "Lanzando RMI registry"
rmiregistry &
echo
echo "Compilando archivos .java"
javac *.java
sleep 1
echo
echo "Lanzando servidor"
java -cp . -Djava.rmi.server.codebase=file:./ -Djava.rmi.server.hostname=localhost -Djava.security.policy=server.policy Ejemplo
