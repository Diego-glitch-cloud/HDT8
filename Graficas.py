import pandas as pd
import matplotlib.pyplot as plt

# Se lee el csv del archivo de simulacion
df = pd.read_csv("ResultadosHospital.csv")

# Se ordena por ID para mostrar la grafica ordenada
df = df.sort_values("IDPaciente")

# se configura el tamaño
plt.figure(figsize=(10, 5))

# se genera el tipo de grafica
plt.scatter(df["IDPaciente"], df["TiempoTotal"], color="blue", alpha=0.6, label="Puntos")

# se une para hacer un mejor analisis
plt.plot(df["IDPaciente"], df["TiempoTotal"], color="orange", linewidth=1, label="Línea")

# se configuran los ejes y aspectos visuales
plt.xlabel("Paciente por ID")
plt.ylabel("Tiempo total en el hospital en mins")
plt.title("Tiempo por paciente en el hospital")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
