import simpy
import random
import csv
import os

# Parámetros del hospital
LlegadaDePacientes = 5
TiempoDeTriage = 10
TiempoDeConsulta = 15
TiempoDeLab = 20
Enfermeras = 2
Doctores = 3
LaboratoriosDisponibles = 1
TiempoDeSimulacion = 200  

# Función para registrar datos en CSV
def registrar_datos(datos):
    archivo_nuevo = not os.path.exists("resultados.csv")
    with open("resultados.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if archivo_nuevo:
            writer.writerow(["ID", "Severidad", "T_Llegada", "T_Triage", "T_Consulta", "T_Laboratorio", "T_Salida"])
        writer.writerows(datos)

# Función para generar pacientes
def generar_pacientes(env, hospital, datos):
    paciente_id = 0
    while True:
        severidad = random.randint(1, 5)  # 1 es el más grave, 5 el menos grave
        env.process(proceso_paciente(env, hospital, paciente_id, severidad, datos))
        paciente_id += 1
        yield env.timeout(random.expovariate(1.0 / LlegadaDePacientes))

# Función del flujo del paciente
def proceso_paciente(env, hospital, paciente_id, severidad, datos):
    llegada = env.now

    # Etapa 1: Triage
    with hospital["enfermeras"].priority_request(priority=severidad) as req:
        yield req
        inicio_triage = env.now
        yield env.timeout(random.normalvariate(TiempoDeTriage, 2))  # Variabilidad en el tiempo de triage
        fin_triage = env.now

    # Etapa 2: Consulta con doctor
    with hospital["doctores"].priority_request(priority=severidad) as req:
        yield req
        inicio_consulta = env.now
        yield env.timeout(random.normalvariate(TiempoDeConsulta, 3))  # Variabilidad en consulta
        fin_consulta = env.now

    # Etapa 3: Laboratorio (si aplica)
    inicio_lab = fin_lab = -1
    if random.random() < 0.5:  
        with hospital["laboratorios"].priority_request(priority=severidad) as req:
            yield req
            inicio_lab = env.now
            yield env.timeout(random.normalvariate(TiempoDeLab, 5))  # Variabilidad en laboratorio
            fin_lab = env.now

    # Registrar datos del paciente
    salida = env.now
    datos.append([paciente_id, severidad, llegada, fin_triage, fin_consulta, fin_lab, salida])

# Configuración del hospital
def inicializar_hospital(env):
    return {
        "enfermeras": simpy.PriorityResource(env, capacity=Enfermeras),
        "doctores": simpy.PriorityResource(env, capacity=Doctores),
        "laboratorios": simpy.PriorityResource(env, capacity=LaboratoriosDisponibles)
    }

# Función para calcular estadísticas
def calcular_estadisticas(datos):
    tiempos_triage = [(fila[3] - fila[2]) for fila in datos if fila[3] is not None]  # Triage - Llegada
    tiempos_consulta = [(fila[4] - fila[3]) for fila in datos if fila[4] is not None]  # Consulta - Triage
    tiempos_lab = [(fila[5] - fila[4]) for fila in datos if fila[5] > 0]  # Laboratorio - Consulta

    if tiempos_triage:
        print(f"Tiempo promedio de espera en triage: {sum(tiempos_triage)/len(tiempos_triage):.2f} min")
    if tiempos_consulta:
        print(f"Tiempo promedio de espera en consulta: {sum(tiempos_consulta)/len(tiempos_consulta):.2f} min")
    if tiempos_lab:
        print(f"Tiempo promedio en laboratorio: {sum(tiempos_lab)/len(tiempos_lab):.2f} min")

# Función principal
def main():
    env = simpy.Environment()
    hospital = inicializar_hospital(env)
    datos = []
    env.process(generar_pacientes(env, hospital, datos))
    env.run(until=TiempoDeSimulacion)
    registrar_datos(datos)
    calcular_estadisticas(datos)  # Llamamos la función para mostrar los tiempos promedio

if __name__ == "__main__":
    main()
