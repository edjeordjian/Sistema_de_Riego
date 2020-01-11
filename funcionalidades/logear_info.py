import csv
import os
from datetime import datetime

import serial

from .keypress import KBHit


def logear():
    carpeta = "data"
    fecha_inicio = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print("Logeando informacion, para detener el proceso pulse 'q'...")
    # Se establece la conexion serie
    if os.name == "nt":
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")
    # Vacia el buffer por las dudas
    ser.reset_input_buffer()
    kb = KBHit()
    with open(f"{carpeta}/log.csv", "w+", newline="") as f:
        escritor = csv.writer(f)
        while True:
            # Si ingresaron "q" entonces terminar de logear
            if kb.kbhit() and kb.getch() == "q":
                kb.set_normal_term()
                break
            try:
                # Leer una linea del output del arduino
                ser_bytes = ser.readline().decode()
                _, humedad, _, luz, estado = ser_bytes.rstrip().split()
                estado = int(estado)
                # Para logear la hora, minutos y segundos junto con cada
                # medicion
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d;%H:%M:%S")
                # El estado es 0 si esta abierto, y 1 si esta cerrado
                abierto = "Abierto" if estado else "Cerrado"
                escritor.writerow([current_time, humedad, luz, abierto])
            except BaseException:
                print("Keyboard Interrupt")
                break
    fecha_final = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    old_file = os.path.join(carpeta, "log.csv")
    new_file = os.path.join(carpeta, f"{fecha_inicio}__{fecha_final}.csv")
    os.rename(old_file, new_file)
