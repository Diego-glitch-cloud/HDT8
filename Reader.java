import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Reader {
    public List<Paciente> leerPacientes(String filePath) {
        List<Paciente> pacientes = new ArrayList<>();
        
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                // Dividir la línea por comas
                String[] datos = line.split(",", 3); // Máximo 3 partes (nombre, síntoma, prioridad)
                
                if (datos.length == 3) {
                    // Elimina los espacios al inicio y al final del string
                    String nombre = datos[0].trim();
                    String sintoma = datos[1].trim();
                    String prioridad = datos[2].trim();
                    
                    // Crear nuevo paciente y agregarlo a la lista
                    Paciente paciente = new Paciente(nombre, sintoma, prioridad);
                    pacientes.add(paciente);
                }
            }
        } catch (IOException e) {
            System.err.println("Error al leer el archivo: " + e.getMessage());
        }
        
        return pacientes;
    }
}