# Descricpión
La idea es poder regar una planta de forma automatizada utilizando sensores que verifiquen las condiciones adecuadas para el regado: poca humedad y poca luz. Para eso se utiliza un fotorresistor y un sensor de humedad. Adicionalmente, se construye un programa para el monitoreo de los valores registrados, asi como para configuración de los valores precisos para considerar los valores mínimos aceptables de humedad y luz.

# Componentes
- Arduino ESP8266 (Lolin Nodemcu v3)
- Fotoresistor GL5537
- Sensor de humedad HL-69
- Electroválvula XJD-33
- Relé SRV-05
- Multiplexor 4051 (CD4051BD) (para aprovechar el úncio pin analógico) 

# Circuito
![alt text](media/circuito1.png)

![alt text](media/pinout.jpg)
![alt text](media/placa2.png)
![alt text](media/placa1.png)

# Previsualización
El menu del software es el siguiente:
![alt text](media/menu.png)

una de las características salientes es la visualización en vivo de los valores de luz y humedad captados por los sensores:
![alt text](media/arduino1.gif)

puede verse como disminuyendo el nivel de luz, se activa la electroválvula que permite el regado de la planta
![alt text](media/arduino2.gif)

# ¿Qué se necesita para correrlo?
El software requiere del circuito conectado a la computadora, junto con python 3 y los módulos: pyserial, numpy y tabulate. 
