public class Paciente implements Comparable<Paciente> { // Especifica el tipo genérico

    // Atributos
    String nombre;
    String sintoma;
    char codigo;

    // Constructor
    public Paciente(String nombre, String sintoma, char codigo) {
        this.nombre = nombre;
        this.sintoma = sintoma;
        this.codigo = codigo;
    }

    // Getters y setters
    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getSintoma() {
        return sintoma;
    }

    public void setSintoma(String sintoma) {
        this.sintoma = sintoma;
    }

    public char getCodigo() {
        return codigo;
    }

    public void setCodigo(char codigo) {
        this.codigo = codigo;
    }

    @Override
    public int compareTo(Paciente otro) {
        // Compara por código de prioridad
        return Character.compare(this.codigo, otro.codigo);
    }

    @Override
    public String toString() {
        return "Paciente{" +
            "nombre='" + nombre + '\'' +
            ", sintoma='" + sintoma + '\'' +
            ", codigo=" + codigo +
            '}';
    }
}