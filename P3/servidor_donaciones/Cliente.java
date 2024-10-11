import java.rmi.registry.LocateRegistry;
import java.rmi.*;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class Cliente {

    public static void main(String[] args) {
        String idReplica = "replica1"; //Por defecto conecta a la primera replica

        if(args.length == 1) idReplica = args[0]; //Se puede elegir entre cualquier repluia disponible
        
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new SecurityManager());
        }
        try {            
            Registry registry = LocateRegistry.getRegistry("127.0.0.1", 1099);
            interfazClienteServidor servidorDonaciones = (interfazClienteServidor) registry.lookup(idReplica);

            System.out.println("Conexión a servidor: " + idReplica);
            
            String nombreUsuario = "", contraseña = "";
            boolean sesionIniciada = false;
            char op;
            int cantidad = 0;
            Scanner sc = new Scanner(System.in);

            while(true){
                System.out.println("------------------------------------------------");
                System.out.println("Selecciona una operación:");
                System.out.println("    r - Registrarse");
                System.out.println("    i - Iniciar sesión");
                System.out.println("    d - Realizar una donación");
                System.out.println("    e - Ver cantidad donada");
                System.out.println("    n - Ver cuantas donaciones he realizado");
                System.out.println("    t - Ver total donado");
                System.out.println("    l - Ver lista completa de donantes");
                System.out.println("    c - Cerrar sesion");
                System.out.println("    s - Salir");
                
                op = sc.next().charAt(0);

                if(op == 's')
                    break;

                switch (op) {
                    case 'r':
                        System.out.print("Registro de usuario.\nNombre de usuario: ");
                        sc.nextLine();
                        nombreUsuario = sc.nextLine();
                        System.out.print("Contraseña: ");
                        contraseña = sc.nextLine();
                        if(servidorDonaciones.registrarCliente(nombreUsuario, contraseña))
                            System.out.println("Usuario ya registrado");  

                        sesionIniciada = servidorDonaciones.iniciarSesionCliente(nombreUsuario, contraseña);
                        if(sesionIniciada)
                            System.out.println("Sesión iniciada correctamente");  

                        break;
                        
                    case 'i':                        
                        if(!sesionIniciada){
                            System.out.print("Nombre de usuario: ");
                            sc.nextLine();
                            nombreUsuario = sc.nextLine();
                            System.out.print("Contraseña: ");
                            contraseña = sc.nextLine();
                            sesionIniciada = servidorDonaciones.iniciarSesionCliente(nombreUsuario, contraseña);
                        }
                        
                        if(sesionIniciada)
                            System.out.println("Ya has iniciado sesión, si quieres acceder con otro usuario cierra sesión.");  
                        else
                            System.out.println("\nUsuario o contraseña incorrectos");  
                        break;
                    
                    case 'd':
                        if(sesionIniciada){
                            System.out.print("Cantidad para donar: ");
                            cantidad = sc.nextInt();
                            if(cantidad > 0){
                                if(servidorDonaciones.donar(nombreUsuario, contraseña, cantidad))
                                    System.out.println("Donación completada");
                            } else {
                                System.out.println("No se puede donar un numero negativo");
                            }
                        } else
                            System.out.println("Hay que estar registrado para donar");
                        break;
                    
                    case 'e':
                        if(sesionIniciada){
                            System.out.println(nombreUsuario + " has donado: " + servidorDonaciones.totalDonadoUsuario(nombreUsuario, contraseña) + "€");
                        } else
                            System.out.println("Hay que estar registrado para ver cuanto has donado");
                        break;

                    case 'n':
                        if(sesionIniciada){
                            System.out.println("\nHas donado " + servidorDonaciones.numeroDonacionesRealizadas(nombreUsuario, contraseña) + " veces");
                        } else
                            System.out.println("Hay que estar registrado para ver cuanto has donado");
                        break;
                    
                    case 't':
                        if(sesionIniciada){
                            System.out.println("Total donado: " + servidorDonaciones.totalDonado() + "€");
                        } else
                            System.out.println("Hay que estar registrado para ver el total donado");
                        break;

                    case 'l':
                        if(sesionIniciada){
                            System.out.println("Lista de donantes: \n" + servidorDonaciones.listaDonantes());
                        } else
                            System.out.println("Hay que estar registrado para ver la lista de donantes");
                        break;

                    case 'c':
                        nombreUsuario = "";
                        contraseña = "";
                        sesionIniciada = false;
                        System.out.println("Sesión cerrada");
                        break;

                    default:
                        System.out.println("Carácter no valido, intentalo de nuevo: ");
                        break;
                
                }
            }
        } catch (NotBoundException | RemoteException e) {
            System.err.println("Exception del sistema: " + e);
        }
        System.exit(0);
    }
}