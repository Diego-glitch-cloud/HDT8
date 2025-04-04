import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("ResultadosHospital.csv")

# Ordenar por ID por si no está ordenado (opcional pero recomendado)
df = df.sort_values("ID_Paciente")

# Crear figura
plt.figure(figsize=(10, 5))

# Puntos
plt.scatter(df["ID_Paciente"], df["Tiempo_Total"], color="blue", alpha=0.6, label="Puntos")

# Línea que los une
plt.plot(df["ID_Paciente"], df["Tiempo_Total"], color="orange", linewidth=1, label="Línea")

# Estética
plt.xlabel("ID del Paciente")
plt.ylabel("Tiempo Total en el Hospital (min)")
plt.title("Tiempo Total de Permanencia por Paciente")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
