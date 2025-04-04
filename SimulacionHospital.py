# ------------------------------------------------
# Pedro Caso y Diego Calderón
# Algoritmos y Estructuras de datos
# HDT8
# ------------------------------------------------ 
import simpy
import random
import csv
import os

random.seed(10)
# Parámetros del hospital
LlegadaDePacientes = 5
TiempoDeTriage = 10
TiempoDeConsulta = 15
TiempoDeLab = 20
Enfermeras = 2
Doctores = 3
LaboratoriosDisponibles = 1
TiempoDeSimulacion = 200  

# Función para registrar los datos de la simulacion en el csv
def RegistroDatos(datos):
    NuevoCSV = not os.path.exists("ResultadosHospital.csv") # verifica si el csv ya existe anteriormente para evitar errores
    with open("ResultadosHospital.csv", mode="w", newline="") as file: # abre el archivo y lo ejecuta en modo "writte" y evita lineas en blanco
        modificadorCSV = csv.writer(file) # crea un objeto para escribir en el csv
        if NuevoCSV: # si es nuevo agrega los encabezados y la creacion del csv
            modificadorCSV.writerow(["IDPaciente", "TiempoTotal"])
        modificadorCSV.writerows(datos)

# funcion para simular los pacientes 
def pacientes(env, hospital, datos):
    IDPaciente = 0
    continuar = True
    while continuar:
        gravedad = random.randint(1, 5)  # genera un numero aleatorio del 1 al 5 para ver la gravedad
        env.process(solicitudPaciente(env, hospital, IDPaciente, gravedad, datos)) # envia la solicitud con la gravedad asignada
        IDPaciente += 1 # por cada paciente se va sumando el ID para evitar repetidos
        yield env.timeout(random.expovariate(1.0 / LlegadaDePacientes)) # genera un tiempo aleatorio entre llegadas basado en la tasa promedio de llegada de pacientes

# Función del flujo del paciente
def solicitudPaciente(env, hospital, IDPaciente, gravedad, datos):
    llegada = env.now # se registra el tiempo de llegada del paciente

    # triage o evaluacion 
    with hospital["enfermeras"].request(priority=gravedad) as solicitud: # se identifica la gravedad para identficar la prioridad
        yield solicitud # la solicitud espera hasta encontrar una enfermera disponible
        yield env.timeout(random.normalvariate(TiempoDeTriage, 2))  # se simula el tiempo de evaluacion 

    # consulta con el doctor
    with hospital["doctores"].request(priority=gravedad) as solicitud: # se identifica la gravedad para identficar la prioridad 
        yield solicitud # la solicitud espera hasta encontrar un doctor disponible
        yield env.timeout(random.normalvariate(TiempoDeConsulta, 3))  # se simula el tiempo que pasa el paciente en consulta

    # analisis de laboratorio
    if random.random() < {1: 0.8, 2: 0.6, 3: 0.4, 4: 0.2, 5: 0.1}.get(gravedad, 0.1):  # Probabilidad de laboratorio depende de la gravedad
        with hospital["laboratorios"].request(priority=gravedad) as solicitud:
            yield solicitud  # La solicitud espera hasta encontrar un espacio en el laboratorio
            yield env.timeout(random.normalvariate(TiempoDeLab, 5))  # Se simula el tiempo que pasa en el laboratorio

    # Se registra el tiempo total en el hospital
    salida = env.now
    TiempoTotal = salida - llegada
    datos.append([IDPaciente, TiempoTotal])

# Se configuta el hospital
def inicializar_hospital(env):
    return {
        "enfermeras": simpy.PriorityResource(env, capacity=Enfermeras),
        "doctores": simpy.PriorityResource(env, capacity=Doctores),
        "laboratorios": simpy.PriorityResource(env, capacity=LaboratoriosDisponibles)
    }

# Función para calcular estadísticas
def calcular_estadisticas(datos):
    tiemposTotales = [fila[1] for fila in datos]
    if tiemposTotales:
        print(f"Tiempo promedio del hospital atendiendo: {sum(tiemposTotales)/len(tiemposTotales):.2f} mins")

# Función principal manejando el hospital y mostrar datos
def main():
    env = simpy.Environment()
    hospital = inicializar_hospital(env)
    datos = []
    env.process(pacientes(env, hospital, datos))
    env.run(until=TiempoDeSimulacion)
    RegistroDatos(datos)
    calcular_estadisticas(datos) 

main()

