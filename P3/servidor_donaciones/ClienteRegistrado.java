public class ClienteRegistrado {
    private String nombre, contraseña;
    private int nDonaciones;
    private int totalDonado;

    public ClienteRegistrado(String nombre, String contraseña){
        this.nombre = nombre;
        this.contraseña = contraseña;
        this.totalDonado = 0;
        this.nDonaciones = 0;
    }

    public void registrarDonacion(int n){
        totalDonado += n;
        nDonaciones++;
    }

    public String getNombre(){
        return nombre;
    }

    public String getContraseña(){
        return contraseña;
    }

    public int getNumeroDonaciones(){
        return nDonaciones;
    }

    public int getTotalDonado(){
        return totalDonado;
    }

    public boolean esDonador(){
        return nDonaciones > 0;
    }
}
