import static org.junit.Assert.*;
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
        VectorHeap<Paciente> heap = new VectorHeap<>();
        
        Paciente pA = new Paciente("Test A", "Test", 'A');
        Paciente pB = new Paciente("Test B", "Test", 'B');
        
        heap.add(pB);
        heap.add(pA);
        
        // A tiene mayor prioridad que B
        assertEquals(pA, heap.remove());
        assertEquals(pB, heap.remove());
        assertTrue(heap.isEmpty());
    }
    
    @Test
    public void testPrioridades() {
        VectorHeap<Paciente> heap = new VectorHeap<>();
        
        Paciente pA = new Paciente("Test A", "Test", 'A');
        Paciente pB = new Paciente("Test B", "Test", 'B');
        Paciente pC = new Paciente("Test C", "Test", 'C');
        Paciente pD = new Paciente("Test D", "Test", 'D');
        Paciente pE = new Paciente("Test E", "Test", 'E');
        
        // orden inverso
        heap.add(pE);
        heap.add(pD);
        heap.add(pC);
        heap.add(pB);
        heap.add(pA);
        
        // salir en orden de prioridad
        assertEquals(pA, heap.remove());
        assertEquals(pB, heap.remove());
        assertEquals(pC, heap.remove());
        assertEquals(pD, heap.remove());
        assertEquals(pE, heap.remove());
    }
}