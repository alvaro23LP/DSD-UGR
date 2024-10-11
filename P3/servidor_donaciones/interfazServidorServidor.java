import java.rmi.RemoteException;
import java.util.ArrayList;

public interface interfazServidorServidor extends interfazClienteServidor{
    public ArrayList<ClienteRegistrado> getRegistrados() throws RemoteException;
    public void registrarClienteReplica(String nombre, String contraseña) throws RemoteException;
    public void donarReplica(String nombre, String contraseña, int valor) throws RemoteException;
    public int numeroDeRegistrados() throws RemoteException;
    public boolean comprobarRegistro(String nombre, String contraseña) throws RemoteException;
    public void registarDonacionUsuario(String nombre, String contraseña, int valor) throws RemoteException;
    public boolean getEsDonadorUsuario(String nombre, String contraseña) throws RemoteException;
    public int getTotalDonadoUsuario(String nombre, String contraseña) throws RemoteException;
    public int getNumeroDonacionesUsuario(String nombre, String contraseña) throws RemoteException;
    public int getTotalDonadoLocal() throws RemoteException;
    public int getTotalDonado() throws RemoteException;
    public String listaDonantesLocal() throws RemoteException;
}
