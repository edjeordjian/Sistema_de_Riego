import _tkinter
import csv
import os
import time
import matplotlib.pyplot as plt
import gc

import serial
from tabulate import tabulate

from funcionalidades.cargar_visualizar_datos import cargar_visualizar
from funcionalidades.logear_info import logear
from funcionalidades.visualizar_tiempo_real import tiempo_real

CANTIDAD_DE_OPCIONES = 7
CARPETA_DATOS = "data"
CARPETA_PLANTAS = "plantas"
CONFIGURACIONES = "valores_limite.riego"
LOGEAR = True


def menu():

    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    humedad = 800
    luz = 300
    # Creamos la carpeta de datos si no existe
    if not os.path.isdir(CARPETA_DATOS):
        os.mkdir(CARPETA_DATOS)

    if not os.path.isdir(CARPETA_PLANTAS):
        os.mkdir(CARPETA_PLANTAS)

    if os.path.isfile(CONFIGURACIONES):
        archivo = open(CONFIGURACIONES)
        linea = archivo.readline().split()
        humedad, luz = map(float, linea)
        ser.write(f"m{humedad}l{luz}".encode())
        archivo.close()

    os.system("cls" if os.name == "nt" else "clear")
    funcionalidades = [
        log_info,
        visualizar_tiempo_real,
        visualizar_local,
        controlar,
        cambiar_configuracion,
        alta_baja_plantas,
    ]
    
    ser.close()
    opcion = 0
    
    while opcion != CANTIDAD_DE_OPCIONES:
        mostrar_opciones()
        opcion = input("Insertar el número de accion deseada: ")

        os.system("cls" if os.name == "nt" else "clear")

        opcion = validar(opcion, 1, CANTIDAD_DE_OPCIONES)
        if opcion is None or opcion == CANTIDAD_DE_OPCIONES:
            continue
        if opcion == 5:
            humedad, luz = cambiar_configuracion(humedad, luz)
            continue
        if opcion == 6:
            humedad,luz = alta_baja_plantas(humedad, luz)
            continue
        funcionalidades[opcion - 1]()
    with open(CONFIGURACIONES, "w+") as f:
        f.write(f"{humedad} {luz}")


def log_info():
    global LOGEAR
    print(f"Se ha {'des'*LOGEAR}activado el logeo de informacion\n")
    LOGEAR = not LOGEAR
    return


def visualizar_tiempo_real():
    eleccion = tomar_intervalo_tiempo()

    print("Mostrando informacion sensores, presione 'q' para volver al menu")

    tiempo_real(eleccion, LOGEAR)
    plt.close('all')
    os.system("cls" if os.name == "nt" else "clear")


def visualizar_local():
    intervalo = tomar_intervalo_tiempo()
    n_archivo = -1
    while n_archivo != 0:
        os.system("cls" if os.name == "nt" else "clear")

        print(
            f"ATENCIÓN: los archivos de log se encuentran en la carpeta {CARPETA_DATOS}"
        )
        # files = filter(os.path.isfile, os.listdir(CARPETA_DATOS))
        files = os.listdir(CARPETA_DATOS)
        files = [os.path.join(CARPETA_DATOS, f)
                 for f in files]  # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))

        for i, f in enumerate(files):
            print(f"{i+1}) {f}")

        n_archivo = input(
            "Elegir el número de archivo que quiere visualizar, o 0 para volver al menú: "
        )
        n_archivo = validar(n_archivo, 0, len(files))

        if n_archivo is None or n_archivo == 0:
            continue
        try:
            cargar_visualizar(files[n_archivo - 1], intervalo)

        except FileNotFoundError:
            input("Archivo no encontrado. Presione enter para continuar")

    os.system("cls" if os.name == "nt" else "clear")


def controlar():
    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    eleccion = 0
    while eleccion != 3:
        print("1) Abrir válvula")
        print("2) Cerrar válvula")
        print("3) Volver al menú principal")
        print()
        eleccion = input("Seleccionar una opción: ")
        print()
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 1, 3)
        if eleccion is None:
            continue
        if eleccion == 1:
            ser.write("a".encode())
        elif eleccion == 2:
            ser.write("c".encode())
        else:
            ser.write("n".encode())
            # Se vuelve al flujo normal una vez se sale de la funcion


def cambiar_configuracion(humedad, luz):
    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    v_humedad = {481: 95, 595: 75, 738: 50, 881: 25, 995: 5}

    eleccion = 0
    while eleccion != 3:
        print("1) Configurar nivel de humedad")
        print("2) Configurar nivel de luz")
        print("3) Volver al menú principal")
        print("-" * 20)
        print(
            f"El limite actual de luz es: {luz} y el limite de humedad es de: {v_humedad[humedad]}%"
        )

        eleccion = input("Seleccionar una opción: ")
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 1, 3)

        if eleccion is None:
            continue
        if eleccion == 1:
            humedad = configurar_humedad(ser, True, humedad)
        elif eleccion == 2:
            luz = configurar_luz(ser, True, luz)
        else:
            pass
    return humedad, luz


def configurar_humedad(ser, impactar, hum_act):
    # ecuación para despejar según los valores observados empíricamente:
    # valor_array = porcentaje * max_tasa + max_humedad
    # hrd cd
    # max_tasa: 572
    # max_humedad: 452
    # porcentaje: entre 0 y 1, según el nivel querido, donde
    # un porcentaje alto indica mucha humedad

    valores_humedad = [481, 595, 738, 881, 995]  # dupli
    v_humedad = {0: 95, 1: 75, 2: 50, 3: 25, 4: 5}
    eleccion = 0
    while eleccion != 6:
        print("1) Muy húmedo [95%]")
        print("2) Húmedo [75%]")
        print("3) Intermedio [50%]")
        print("4) Seco [25%]")
        print("5) Muy seco [5%]")
        print("6) Volver atrás")
        print()
        eleccion = input(
            "Elegir la opción de humedad para la activación de la válvula: ")
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 1, 6)

        if impactar:
            if eleccion is None or eleccion == 6:
                continue
            else:
                ser.write(f"h{valores_humedad[eleccion-1]}".encode())
                hum_act = valores_humedad[eleccion - 1]
                print()
                print("Humedad configurada correctamente\n")

        else:
            if eleccion is None:
                continue
            else:
                return v_humedad[eleccion - 1] if eleccion != 6 else -1

    return hum_act


def configurar_luz(ser, impactar, luz_act):
    eleccion = 0
    while eleccion != -1:
        eleccion = input(
            "Elegir el valor en lux de luz límite para la válvula (valor entre 0 y 1023) o ingresar -1 para salir: "
        )
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, -1, 1023)

        if impactar:
            if eleccion is None or eleccion == -1:
                continue
            else:
                luz_act = eleccion
                ser.write(f"l{eleccion}".encode())
                print("Niveles de luz configurados correctamente\n")

        else:
            if eleccion is None:
                continue
            else:
                return eleccion
    return luz_act


def alta_baja_plantas(humedad, luz):
    plantas = []
    if os.path.isfile(f"{CARPETA_PLANTAS}/presets.planta"):
        with open(f"{CARPETA_PLANTAS}/presets.planta", "r") as f:
            lector = csv.reader(f)
            for planta in lector:
                plantas.append(planta)

    eleccion = None
    while eleccion != 5:
        print("1) Ver listado de configuraciones de plantas")
        print("2) Utilizar configuración de planta específica")
        print("3) Agregar configuraciones de planta")
        print("4) Eliminar configuraciones de planta")
        print("5) Volver al menú")
        print()
        eleccion = input("Elija una opción: ")
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 1, 5)

        if eleccion == 1:
            mostrar_plantas(plantas)
        elif eleccion == 2:
            if len(plantas) == 0:
                print("No hay plantas en el sistema de las cuales elegir!\n")
                continue
            humedad, luz = cargar_preset(plantas)
        elif eleccion == 3:
            alta_planta(plantas)
        elif eleccion == 4:
            if len(plantas) == 0:
                print("No hay plantas en el sistema!\n")
                continue
            baja_planta(plantas)


    with open(f"{CARPETA_PLANTAS}/presets.planta", "w+", newline="") as f:
        escritor = csv.writer(f)
        for planta in plantas:
            if planta and planta != "\r\n":  # Windows
                escritor.writerow(planta)

    return humedad,luz

def mostrar_plantas(listado_plantas):
    printable_plantas = [[i] + planta
                         for i, planta in enumerate(listado_plantas)]
    print(
        tabulate(
            printable_plantas,
            headers=["ID", "Planta", "Humedad limite [%]", "Luz limite [lux]"],
        ))
    print()


def cargar_preset(plantas):
    v_humedad = {"95": 481, "75": 595, "50": 738, "25": 881, "5": 995}  # dupl

    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    eleccion = None
    while eleccion == None:
        mostrar_plantas(plantas)
        print()
        eleccion = input(
            "Elegir el número de la configuración de planta que desea cargar: "
        )
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 0, len(plantas) - 1)
        if eleccion is None:
            continue
    planta = plantas[eleccion]
    ser.write(f"m{int( v_humedad[ planta[1] ] )}l{int(planta[2])}".encode())

    print("Configuración de planta cargada correctamente\n")
    return v_humedad[planta[1]], planta[2]


def alta_planta(plantas):
    nombre = input("Ingresar el nombre de la planta: ")
    os.system("cls" if os.name == "nt" else "clear")

    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    humedad = None
    while humedad == None:
        os.system("cls" if os.name == "nt" else "clear")
        humedad = configurar_humedad(ser, False, None)

    if humedad == -1:
        return

    luz = None
    while luz == None:
        os.system("cls" if os.name == "nt" else "clear")
        luz = configurar_luz(ser, False, None)

    if luz == -1:
        return

    plantas.append([nombre, humedad, luz])
    print("Planta agregada correctamente")
    print()


def baja_planta(plantas):
    eleccion = None
    while eleccion == None:
        mostrar_plantas(plantas)
        print()
        eleccion = input("Elegir el id de la planta que desea borrar: ")
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 0, len(plantas) - 1)
        if eleccion is None:
            continue
    plantas.pop(eleccion)
    print("Planta eliminada correctamente!\n")


def mostrar_opciones():
    print()
    print("-" * 40)
    print(
        "1) Activar/desactivar el logeo de informacion (por defecto esta activado)"
    )
    print("2) Visualizar datos en tiempo real")
    print("3) Visualizar datos desde un archivo de log")
    print("4) Control manual de la válvula")
    print("5) Cambiar valores de activacion de la válvula")
    print("6) Cargar, agregar o borrar configuraciones de plantas")
    print("7) Salir del programa")
    print("-" * 40)
    print()


def validar(eleccion, r_min, r_max):
    try:
        int(eleccion)
    except (ValueError, TypeError):
        print()
        print("No se ha insertado un número")
        print()
        return None

    eleccion = int(eleccion)

    if eleccion < r_min or eleccion > r_max:
        print()
        print("ERROR: El número insertado no esta en el rango posible")
        print()
        return None

    return eleccion


def tomar_intervalo_tiempo():
    eleccion = None
    while eleccion == None:
        print()
        eleccion = input(
            "Elegir el período de tiempo en segundos que se desea visualizar en pantalla (entre 5 y 86 400): "
        )
        os.system("cls" if os.name == "nt" else "clear")
        eleccion = validar(eleccion, 5, 86400)  # Max un dia

    return eleccion

try:
    menu()

except serial.SerialException:
    print()
    print("ERROR: el Arduino está inaccesible.")
    print()
