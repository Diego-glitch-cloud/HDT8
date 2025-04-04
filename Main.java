import java.util.List;

public class Main {
    public static void main(String[] args) {
        System.out.println("USANDO VECTORHEAP");
        
        // Leer pacientes del archivo
        Reader reader = new Reader();
        List<Paciente> listaPacientes = reader.leerPacientes("pacientes.txt");

        // VECTORHEAP
        VectorHeap<Paciente> colaVectorHeap = new VectorHeap<>();
        
        // Agregar pacientes a la cola
        for (Paciente paciente : listaPacientes) {
            colaVectorHeap.add(paciente);
        }
        
        // Mostrar pacientes en orden de prioridad
        while (!colaVectorHeap.isEmpty()) {
            Paciente siguiente = colaVectorHeap.remove();
            System.out.println(siguiente.toString());
        }
// --------------------------------------------------------------------------------------------        
       
        // Segunda implementación 
        System.out.println("\n\nUSANDO JAVA COLLECTION FRAMEWORK");
        
        // JAVA COLLECTION FRAMEWORK
        java.util.PriorityQueue<Paciente> colaPrioridad = new java.util.PriorityQueue<>();
        
        // Agregar pacientes a la cola
        for (Paciente paciente : listaPacientes) {
            colaPrioridad.add(paciente);
        }
        
        // Mostrar pacientes en orden de prioridad
        while (!colaPrioridad.isEmpty()) {
            Paciente siguiente = colaPrioridad.poll();
            System.out.println(siguiente.toString());
        }
    }
}