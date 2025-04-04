import java.util.Vector;

public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    private Vector<E> data = new Vector<>();

    // Métodos auxiliares para obtener los índices de la estructura de heap

    // Indice de un nodo padre dado el índice del nodo hijo
    private int padre(int pos) {
        return (pos - 1) / 2;
    }

    // Dado el index del nodo padre, se da el index del nodo hijo izquierdo
    private int hijoIzquierdo(int pos) {
        return 2 * pos + 1;
    }

    // Dado el index del nodo padre, se da el index del nodo hijo derecho
    private int hijoDerecho(int pos) {
        return 2 * pos + 2;
    }

    // Método para intercambiar elementos en el vector
    private void swap(int i, int j) {
        E temp = data.get(i);
        data.set(i, data.get(j));
        data.set(j, temp);
    }

    @Override
    public void add(E value) {
        data.add(value);
        int actual = data.size() - 1;
        // Subir el elemento hasta restaurar el heap
        while (actual > 0 && data.get(actual).compareTo(data.get(padre(actual))) < 0) {
            swap(actual, padre(actual));
            actual = padre(actual);
        }
    }

    @Override
    public E remove() {
        if (data.isEmpty()) {
            return null;
        }

        E resultado = data.get(0);
        E ultimo = data.remove(data.size() - 1);

        if (!data.isEmpty()) {
            data.set(0, ultimo);
            int actual = 0;
            // Bajar el elemento para mantener el heap
            while (true) {
                int masPequeño = actual;
                int izq = hijoIzquierdo(actual);
                int der = hijoDerecho(actual);

                if (izq < data.size() && data.get(izq).compareTo(data.get(masPequeño)) < 0) {
                    masPequeño = izq;
                }
                if (der < data.size() && data.get(der).compareTo(data.get(masPequeño)) < 0) {
                    masPequeño = der;
                }
                if (masPequeño == actual) {
                    break;
                }
                swap(actual, masPequeño);
                actual = masPequeño;
            }
        }
        return resultado;
    }

    @Override
    public E peek() {
        return data.isEmpty() ? null : data.get(0);
    }

    @Override
    public boolean isEmpty() {
        return data.isEmpty();
    }

    @Override
    public int size() {
        return data.size();
    }

    @Override
    public void clear() {
        data.clear();
    }
}