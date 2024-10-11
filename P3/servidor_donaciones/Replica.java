import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Replica extends UnicastRemoteObject implements interfazServidorServidor {
    private String idReplica;
    private int totalDonadoLocal;
    private ArrayList<ClienteRegistrado> registrados;
    private ArrayList<interfazServidorServidor> servidores;

    public Replica(String idReplica) throws RemoteException { // Constructor
        this.idReplica = idReplica;
        totalDonadoLocal = 0;
        registrados = new ArrayList<ClienteRegistrado>();
        servidores = new ArrayList<interfazServidorServidor>();
    }

    //////////////////////////// Operaciones clase Replica ////////////////////////////
    public String getId(){
        return idReplica;
    }

    private ClienteRegistrado getUsuario(String nombre, String contraseña){
        for(int i=0 ; i<registrados.size() ; i++)
            if(nombre.equals(registrados.get(i).getNombre()) && contraseña.equals(registrados.get(i).getContraseña()))
                return registrados.get(i);
        return null;
    }

    private interfazServidorServidor getServidorDeUnRegistrado(String nombre, String contraseña) throws RemoteException{
        boolean registrado = comprobarRegistro(nombre, contraseña);
        if(registrado)
            return this;

        for(int i=0 ; i<servidores.size() && !registrado ; i++){
            registrado = servidores.get(i).comprobarRegistro(nombre, contraseña);
            if(registrado)
                return servidores.get(i);
        }
        return null;
    }

    public void aniadirServidor(String nombre){
        try {
            Registry registry = LocateRegistry.getRegistry("127.0.0.1", 1099);
            interfazServidorServidor rep = (interfazServidorServidor) registry.lookup(nombre);
            servidores.add(rep);
        } catch (RemoteException | NotBoundException e) {
            e.printStackTrace();
        }
    }
    
    //////////////////////////// Cliente - Servidor ////////////////////////////
    public boolean registrarCliente(String nombre, String contraseña) throws RemoteException{
        //Compruebo que no este registrado
        boolean registrado = comprobarRegistro(nombre, contraseña);

        for(int i=0 ; i<servidores.size() && !registrado ; i++)
            registrado = servidores.get(i).comprobarRegistro(nombre, contraseña);
        
        if(!registrado){
            int minimoRegistrados = numeroDeRegistrados();
            int nReplica = -1;
            //Buscamos la replica con menor n de usuarios
            for(int i=0 ; i<servidores.size() && !registrado ; i++) 
                if(servidores.get(i).numeroDeRegistrados() < minimoRegistrados){
                    minimoRegistrados = servidores.get(i).numeroDeRegistrados();
                    nReplica = i;
                }
            if(nReplica == -1) registrarClienteReplica(nombre, contraseña);
            else servidores.get(nReplica).registrarClienteReplica(nombre, contraseña);
        }
        return registrado;
    }

    public boolean iniciarSesionCliente(String nombre, String contraseña) throws RemoteException{
        boolean registrado = comprobarRegistro(nombre, contraseña);

        for(int i=0 ; i<servidores.size() && !registrado; i++)
            registrado = servidores.get(i).comprobarRegistro(nombre, contraseña);

        return registrado;
    }

    public boolean donar(String nombre, String contraseña, int n) throws RemoteException {
        boolean completada = false;
        interfazServidorServidor servidorDelUsario = getServidorDeUnRegistrado(nombre, contraseña);
        
        if(n > 0 && servidorDelUsario != null){
            System.out.println("Donación de: " + n + "€");
            servidorDelUsario.donarReplica(nombre, contraseña, n);
            servidorDelUsario.registarDonacionUsuario(nombre, contraseña, n);
            completada = true;
        } 
        else if(n < 0) System.out.println("Intento de donación con saldo negativo en " + idReplica);
        else System.out.println("Usuario no registrado");
        return completada;
    }

    public int totalDonado() throws RemoteException{
        return getTotalDonado();
    }

    public int totalDonadoUsuario(String nombre, String contraseña) throws RemoteException{
        interfazServidorServidor replica = getServidorDeUnRegistrado(nombre, contraseña);
        if(replica != null)
            return replica.getTotalDonadoUsuario(nombre, contraseña);
        return 0;
    }

    public int numeroDonacionesRealizadas(String nombre, String contraseña) throws RemoteException{
        interfazServidorServidor replica = getServidorDeUnRegistrado(nombre, contraseña);
        if(replica != null)
            return replica.getNumeroDonacionesUsuario(nombre, contraseña);
        return 0;
    }

    public String listaDonantes() throws RemoteException{
        String lista = "";
        lista += listaDonantesLocal();
        for(int i=0 ; i<servidores.size(); i++)
            lista += servidores.get(i).listaDonantesLocal();
        return lista;
    }

    
    //////////////////////////// Servidor - Servidor ////////////////////////////
    public ArrayList<ClienteRegistrado> getRegistrados() throws RemoteException {
        return registrados;
    }

    public void registrarClienteReplica(String nombre, String contraseña) throws RemoteException{
        System.out.println("Registro realizado en " + idReplica);
        registrados.add(new ClienteRegistrado(nombre, contraseña));
    }

    public void donarReplica(String nombre, String contraseña, int n) throws RemoteException{
        System.out.println("Nueva donación en: " + idReplica);
        totalDonadoLocal += n;
    }

    public int getTotalDonado() throws RemoteException{
        System.out.println("Solicitud valor total donado.");
        int totalDonado = totalDonadoLocal;
        for(int i=0 ; i<servidores.size() ; i++)
            totalDonado += servidores.get(i).getTotalDonadoLocal();
        return totalDonado;
    }

    public int getTotalDonadoLocal() throws RemoteException{
        return totalDonadoLocal;
    }

    public boolean comprobarRegistro(String nombre, String contraseña) throws RemoteException{
        for(int i=0 ; i<registrados.size() ; i++){
            if(nombre.equals(registrados.get(i).getNombre()) && contraseña.equals(registrados.get(i).getContraseña()))
                return true;
        }
        return false;
    }

    public int numeroDeRegistrados() throws RemoteException{
        return registrados.size();
    }

    public boolean getEsDonadorUsuario(String nombre, String contraseña) throws RemoteException{
        return getUsuario(nombre, contraseña).esDonador();
    }

    public void registarDonacionUsuario(String nombre, String contraseña, int valor) throws RemoteException{
        getUsuario(nombre, contraseña).registrarDonacion(valor);
    }
    
    public int getTotalDonadoUsuario(String nombre, String contraseña) throws RemoteException{
        return getUsuario(nombre, contraseña).getTotalDonado();
    }
    
    public int getNumeroDonacionesUsuario(String nombre, String contraseña) throws RemoteException{
        return getUsuario(nombre, contraseña).getNumeroDonaciones();
    }

    public String listaDonantesLocal() throws RemoteException{
        String lista = "";
        for(int i=0 ; i<registrados.size(); i++){
            if(registrados.get(i).esDonador())
                lista += registrados.get(i).getNombre() + "\n";
        }
        return lista;
    }

 

}