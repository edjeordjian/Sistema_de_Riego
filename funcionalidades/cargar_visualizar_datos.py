import csv
import sys
from datetime import datetime as dt

import matplotlib as mpl
import matplotlib.dates as mdates
# mpl.rcParams['backend'] = "GTK3Agg"
import matplotlib.pyplot as plt


def cargar_visualizar(archivo, intervalo):
    valores_humedad = []
    valores_luz = []
    valores_humedad_on = []
    valores_humedad_off = []
    valores_luz_on = []
    valores_luz_off = []
    tiempo = []
    x_on = []
    x_off = []

    # humedad en un vaso de agua
    max_humedad = 452
    # 1024 - 452: máxima tasa de humedad con respecto a la referencia
    max_tasa = 572

    with open(archivo) as f:
        lector = csv.reader(f)

        for fecha, humedad, luz, estado in lector:
            valores_humedad.append(float(humedad))
            valores_luz.append(float(luz))
            if estado == "Abierto":
                valores_luz_on.append(float(luz))
                valores_humedad_on.append(float(humedad))
                x_on.append(dt.strptime(fecha, "%Y-%m-%d;%H:%M:%S"))
            else:
                valores_luz_off.append(float(luz))
                valores_humedad_off.append(float(humedad))
                x_off.append(dt.strptime(fecha, "%Y-%m-%d;%H:%M:%S"))

            tiempo.append(dt.strptime(fecha, "%Y-%m-%d;%H:%M:%S"))

    x = tiempo

    fig = plt.figure()
    # Para poder poner fechas en el eje X.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=intervalo))
    # Esto es para que las ventanas de humedad y luz se ubiquen en un lugar en particular
    # de la pantalla de forma que no se superpongan entre si.

    # thismanager = fig.canvas.manager
    # thismanager.window.wm_geometry("+0+10")
    # fig.canvas.manager.window.move(0, 0)

    plt.title("LUZ")
    plt.xlabel("Instante")
    plt.ylabel("Nivel de Luz [lux]")
    plt.plot(x, valores_luz)
    plt.scatter(x_off, valores_luz_off, marker="v")
    plt.scatter(x_on, valores_luz_on, marker="^")
    plt.gcf().autofmt_xdate()

    fig = plt.figure()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=intervalo))

    # thismanager.window.wm_geometry("+800+0")
    # fig.canvas.manager.window.move(635, 0)

    plt.title("HUMEDAD")
    plt.xlabel("Instante")
    plt.ylabel("Nivel de Humedad [%]")
    plt.plot(x, valores_humedad)
    plt.scatter(x_off, valores_humedad_off, marker="v")
    plt.scatter(x_on, valores_humedad_on, marker="^")
    plt.gcf().autofmt_xdate()
    plt.show()
