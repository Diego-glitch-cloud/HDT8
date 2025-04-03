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

# Función para registrar los datos de la simulacion en el csv
def RegistroDatos(datos):
    NuevoCSV = not os.path.exists("ResultadosHospital.csv") # verifica si el csv ya existe anteriormente para evitar errores
    with open("ResultadosHospital.csv", mode="a", newline="") as file: # abre el archivo y lo ejecuta en modo "append" y evita lineas en blanco
        modificadorCSV = csv.writer(file) # crea un objeto para escribir en el csv
        if NuevoCSV: # si es nuevo agrega los encabezados y la creacion del csv
            modificadorCSV.writerow(["ID_Paciente", "Gravedad", "Tiempo_Llegada", "Tiempo_Triage", "Tiempo_Consulta", "Tiempo_Laboratorio", "Tiempo_Salida"])
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
        inicioEvaluacion = env.now # se inicia el tiempo de la evaluacion
        yield env.timeout(random.normalvariate(TiempoDeTriage, 2))  # se simula el tiempo de evalucaion 
        finEvaluacion = env.now # se finaliza el tiempo de evaluacion 

    # consulta con el doctor
    with hospital["doctores"].request(priority=gravedad) as solicitud: # se identifica la gravedad para identficar la prioridad 
        yield solicitud # la solicitud espera hasta encontrar un doctor disponible
        InicioConsulta = env.now # se inicia el tiempo de la consulta
        yield env.timeout(random.normalvariate(TiempoDeConsulta, 3))  # se simula el tiempo que pasa el paciente en consulta
        finalConsulta = env.now # se finaliza el tiempo de la consulta

    # analisis de laboratorio
    inicioLab = finalLab = -1

    # Probabilidad de laboratorio depende de la gravedad
    probabilidad_lab = {1: 0.8, 2: 0.6, 3: 0.4, 4: 0.2, 5: 0.1} #la probabilidad de hacerse analisis depende de su prioridad
    probabilidad = probabilidad_lab.get(gravedad, 0.1)  # Si la gravedad no está en el diccionario, por defecto es 0.1

    if random.random() < probabilidad:  # Se compara con la probabilidad según gravedad
        with hospital["laboratorios"].request(priority=gravedad) as solicitud:
            yield solicitud  # La solicitud espera hasta encontrar un espacio en el laboratorio
            inicioLab = env.now  # Se registra el inicio del tiempo de laboratorio
            yield env.timeout(random.normalvariate(TiempoDeLab, 5))  # Se simula el tiempo que pasa en el laboratorio
            finalLab = env.now  # Se registra el final del tiempo de laboratorio


    # Se registran los datos en el CSV
    salida = env.now
    datos.append([IDPaciente, gravedad, llegada, finEvaluacion, finalConsulta, finalLab, salida])

# Se configuta el hospital
def inicializar_hospital(env):
    return {
        "enfermeras": simpy.PriorityResource(env, capacity=Enfermeras),
        "doctores": simpy.PriorityResource(env, capacity=Doctores),
        "laboratorios": simpy.PriorityResource(env, capacity=LaboratoriosDisponibles)
    }

# Función para calcular estadísticas
def calcular_estadisticas(datos):
    tiemposEvaluacion = [(fila[3] - fila[2]) for fila in datos if fila[3] is not None]  # tiempo de evaluacion cmoparado con el de llegada 
    tiemposConsulta = [(fila[4] - fila[3]) for fila in datos if fila[4] is not None]  # Tiempo de consulta comparado con la evaluacion 
    tiemposLaboratorio = [(fila[5] - fila[4]) for fila in datos if fila[5] > 0]  # Tiempo de lab comparado con el de consulta 

    if tiemposEvaluacion:
        print(f"Tiempo promedio de espera en triage: {sum(tiemposEvaluacion)/len(tiemposEvaluacion):.2f} min")
    if tiemposConsulta:
        print(f"Tiempo promedio de espera en consulta: {sum(tiemposConsulta)/len(tiemposConsulta):.2f} min")
    if tiemposLaboratorio:
        print(f"Tiempo promedio en laboratorio: {sum(tiemposLaboratorio)/len(tiemposLaboratorio):.2f} min")

# Función principal manejando el hospital
def main():
    env = simpy.Environment()
    hospital = inicializar_hospital(env)
    datos = []
    env.process(pacientes(env, hospital, datos))
    env.run(until=TiempoDeSimulacion)
    RegistroDatos(datos)
    calcular_estadisticas(datos)  # Llamamos la función para mostrar los tiempos promedio

if __name__ == "__main__":
    main()
