import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("ResultadosHospital.csv")

# Graficar tiempos de espera en cada etapa
plt.figure(figsize=(10, 5))
plt.scatter(df["Gravedad"], df["Tiempo_Triage"] - df["Tiempo_Llegada"], label="Triage", alpha=0.6)
plt.scatter(df["Gravedad"], df["Tiempo_Consulta"] - df["Tiempo_Triage"], label="Consulta", alpha=0.6)
df_lab = df.dropna(subset=["Tiempo_Laboratorio"])
plt.scatter(df_lab["Gravedad"], df_lab["Tiempo_Laboratorio"] - df_lab["Tiempo_Consulta"], label="Laboratorio", alpha=0.6)
plt.xlabel("Gravedad")
plt.ylabel("Tiempo de Espera")
plt.legend()
plt.title("Tiempos de Espera por Gravedad")
plt.show()
