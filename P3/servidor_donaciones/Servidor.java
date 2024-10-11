import java.net.MalformedURLException;
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.ArrayList;

public class Servidor {
    public static void main(String[] args) {
        int numeroReplicas = 2; //Por defecto 2
        if(args.length == 1) 
            numeroReplicas = Integer.parseInt(args[0]);

        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new SecurityManager());
        }
        try {
            Registry reg = LocateRegistry.createRegistry(1099);
            ArrayList<Replica> replicas = new ArrayList<Replica>();
            
            for(int i = 0; i < numeroReplicas; i++){ // Inicializamos las replicas
                Replica replica = new Replica("replica" + (i+1));
                Naming.rebind(replica.getId(), replica);
                replicas.add(replica);
            }

            for(int i=0 ; i<replicas.size() ; i++){ // Conectamos las replicas entre si
                for(int j=0 ; j<replicas.size() ; j++){
                    if(i != j) replicas.get(i).aniadirServidor(replicas.get(j).getId());
                }
            }
            System.out.println("Servidor lanzado.");

        } catch (RemoteException | MalformedURLException e) {
            System.out.println("Exception: " + e.getMessage());
        }
    }
}