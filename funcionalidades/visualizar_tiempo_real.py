import csv
import datetime
import os
import time

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import serial

from .keypress import KBHit


def tiempo_real(plot_window, logear):
    carpeta = "data"

    if os.name == "nt":  # Windows
        ser = serial.Serial("COM3")
    else:
        ser = serial.Serial("/dev/ttyUSB0")

    ser.flushInput()

    # Abrimos el archivo de log si esta activado el modo log
    if logear:
        fecha_inicio = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        archivo = open(f"{carpeta}/log.csv", "w+", newline="")
        escritor = csv.writer(archivo)
    # IMPORTANTE: Esto es la cantidad de segundos que se quieren visualizar
    # Me creo los datos que van a ir en el eje X e Y, inicialmente son valores cualquiera
    # para rellenar
    y_luz = np.array(np.zeros([plot_window]))
    ahora = datetime.datetime.now()
    x_luz = [
        ahora - datetime.timedelta(0, plot_window - n)
        for n in range(1, plot_window + 1)
    ]

    y_hum = np.array(np.zeros([plot_window]))
    x_hum = [
        ahora - datetime.timedelta(0, plot_window - n)
        for n in range(1, plot_window + 1)
    ]

    # Enciende el modo interactivo
    plt.ion()
    fig_luz, ax_luz = plt.subplots()
    line_luz, = ax_luz.plot(y_luz)
    scat_luz_on, = ax_luz.plot(y_luz, lw=0, marker="^")
    scat_luz_off, = ax_luz.plot(y_luz, lw=0, marker="v")
    y_luz_on = y_luz[:]
    y_luz_off = y_luz[:]
    x_luz_on = x_luz[:]
    x_luz_off = x_luz[:]

    plt.title("LUZ")
    plt.xlabel("Instante")
    plt.ylabel("Nivel de Luz [lux]")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gca().xaxis.set_major_locator(
        mdates.SecondLocator(interval=int(plot_window / 5)))

    fig_hum, ax_hum = plt.subplots()
    line_hum, = ax_hum.plot(y_hum)
    scat_hum_on, = ax_hum.plot(y_hum, lw=0, marker="^")
    scat_hum_off, = ax_hum.plot(y_hum, lw=0, marker="v")
    y_hum_on = y_hum[:]
    y_hum_off = y_hum[:]
    x_hum_on = x_hum[:]
    x_hum_off = x_hum[:]

    plt.title("HUMEDAD")
    plt.xlabel("Instante")
    plt.ylabel("Nivel de Humedad [%]")

    # Config_luzura para que se puedan ver bien las fechas en el eje X
    # En la segunda linea, interval es cada cuantos segundos se pone un label
    # sobre el eje X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gca().xaxis.set_major_locator(
        mdates.SecondLocator(interval=int(plot_window / 5)))

    # humedad en un vaso de agua
    max_humedad = 452
    # 1024 - 452: máxima tasa de humedad con respecto a la referencia
    max_tasa = 572
    # 1024: máximo valor observable por el pin analógico

    kb = KBHit()
    while not (kb.kbhit() and kb.getch() == "q"):
        try:
            try:
                ser_bytes = ser.readline().decode()
            except UnicodeDecodeError:  # Windows
                ser_bytes = ser.readline().decode("cp1252").encode("utf-8")

            try:
                decoded_bytes = ser_bytes.rstrip().split()
            except BaseException:
                continue

            _, humedad, _, luz, estado = decoded_bytes
            humedad = abs(max_humedad -
                          (float(humedad) - max_tasa)) / max_tasa * 100
            luz = float(luz)
            estado = int(estado)
            abierto = "Abierto" if estado else "Cerrado"
            tiempo = datetime.datetime.now()
            # Bajo al log
            if logear:
                escritor.writerow([
                    tiempo.strftime("%Y-%m-%d;%H:%M:%S"), humedad, luz, abierto
                ])

            # Actualizo los valores de ambos ejes
            y_luz = np.append(y_luz, luz)
            y_luz = y_luz[1:plot_window + 1]
            x_luz.append(tiempo)
            x_luz = x_luz[1:plot_window + 1]

            y_luz_on = np.append(y_luz_on, luz if estado else None)
            x_luz_on = np.append(x_luz_on, tiempo if estado else None)
            x_luz_on = x_luz_on[1:plot_window + 1]
            y_luz_on = y_luz_on[1:plot_window + 1]

            y_luz_off = np.append(y_luz_off, luz if not estado else None)
            x_luz_off = np.append(x_luz_off, tiempo if not estado else None)
            x_luz_off = x_luz_off[1:plot_window + 1]
            y_luz_off = y_luz_off[1:plot_window + 1]

            y_hum = np.append(y_hum, humedad)
            y_hum = y_hum[1:plot_window + 1]
            x_hum.append(datetime.datetime.now())
            x_hum = x_hum[1:plot_window + 1]
            # Seteo la nueva data
            y_hum_on = np.append(y_hum_on, humedad if estado else None)
            x_hum_on = np.append(x_hum_on, tiempo if estado else None)
            x_hum_on = x_hum_on[1:plot_window + 1]
            y_hum_on = y_hum_on[1:plot_window + 1]

            y_hum_off = np.append(y_hum_off, humedad if not estado else None)
            x_hum_off = np.append(x_hum_off, tiempo if not estado else None)
            x_hum_off = x_hum_off[1:plot_window + 1]
            y_hum_off = y_hum_off[1:plot_window + 1]

            scat_luz_on.set_data(
                [elem for elem in x_luz_on if elem is not None],
                [l for l in y_luz_on if l is not None],
            )
            scat_luz_off.set_data(
                [elem for elem in x_luz_off if elem is not None],
                [l for l in y_luz_off if l is not None],
            )

            scat_hum_on.set_data(
                [elem for elem in x_hum_on if elem is not None],
                [l for l in y_hum_on if l is not None],
            )
            scat_hum_off.set_data(
                [elem for elem in x_hum_off if elem is not None],
                [l for l in y_hum_off if l is not None],
            )

            line_luz.set_data(x_luz, y_luz)
            ax_luz.relim()
            ax_luz.autoscale_view()

            # Redibujar el grafico
            """
            fig_hum.canvas.draw() 
            fig_luz.canvas.flush_events()
            """

            fig_luz.canvas.draw_idle()
            try:
                # plt.pause(0.06)
                fig_luz.canvas.flush_events()
            except:  # Windows
                break

            fig_luz.autofmt_xdate()

            line_hum.set_data(x_hum, y_hum)
            ax_hum.relim()
            ax_hum.autoscale_view()

            # Redibujar el grafico
            # fig_hum.canvas.draw()
            # fig_hum.canvas.flush_events()

            fig_hum.canvas.draw_idle()
            try:
                # plt.pause(0.05)
                fig_hum.canvas.flush_events()
            except:  # Windows
                break

            fig_hum.autofmt_xdate()

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

    if logear:
        fecha_final = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        archivo.close()
        old_file = os.path.join(carpeta, "log.csv")
        new_file = os.path.join(carpeta, f"{fecha_inicio}__{fecha_final}.csv")
        os.rename(old_file, new_file)


    ax_luz.cla()
    ax_hum.cla()
    fig_hum.clf()
    fig_luz.clf()
    plt.close("all")
    del fig_luz
    del fig_hum
    plt.ioff()
    kb.set_normal_term()
