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
}