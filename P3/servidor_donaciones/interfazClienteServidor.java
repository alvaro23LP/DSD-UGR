import java.rmi.Remote;
import java.rmi.RemoteException;

public interface interfazClienteServidor extends Remote {
    public boolean registrarCliente(String nombre, String contraseña) throws RemoteException;
    public boolean iniciarSesionCliente(String nombre, String contraseña) throws RemoteException;
    public boolean donar(String nombre, String contraseña, int n) throws RemoteException;
    public int totalDonado() throws RemoteException;
    public int totalDonadoUsuario(String nombre, String contraseña) throws RemoteException;
    public int numeroDonacionesRealizadas(String nombre, String contraseña) throws RemoteException;
    public String listaDonantes() throws RemoteException;
}