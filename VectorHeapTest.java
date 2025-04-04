import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.Test;

public class VectorHeapTest {
    
    @Test
    public void testAdd() {
        VectorHeap<Paciente> heap = new VectorHeap<>();
        Paciente p = new Paciente("Test", "Test", 'A');
        heap.add(p);
        assertEquals(p, heap.peek());
    }
    

    @Test
    public void testRemove() {
        // Crear una instancia de VectorHeap con elementos tipo Paciente
        VectorHeap<Paciente> heap = new VectorHeap<>();
        
        // Crear instancias de Paciente
        Paciente pA = new Paciente("Test A", "Dolor de cabeza", 'A');
        Paciente pB = new Paciente("Test B", "Fractura", 'B');
        
        // Agregar los pacientes al heap
        heap.add(pB); // Prioridad 'B'
        heap.add(pA); // Prioridad 'A' (mayor prioridad)

        // Comprobar que se elimina en orden de prioridad
        assertEquals(pA, heap.remove()); // Primero debe salir pA (prioridad 'A')
        assertEquals(pB, heap.remove()); // Luego debe salir pB (prioridad 'B')

        // Comprobar que el heap ahora está vacío
        assertTrue(heap.isEmpty());
    }
}