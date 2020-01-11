# Descricpión
La idea es poder regar una planta de forma automatizada utilizando sensores que verifiquen las condiciones adecuadas para el regado: poca humedad y poca luz. Para eso se utiliza un fotorresistor y un sensor de humedad, y adicionalmente un software para el monitoreo de los valores registrados, asi como la configuración de los valores precisos para considerar los valores aceptables mínimos de humedad y luz.

# Componentes
- Arduino ESP8266 (Lolin Nodemcu v3)
- Fotoresistor GL5537
- Sensor de humedad HL-69
- Electroválvula XJD-33
- Relé SRV-05
- Multiplexor 4051 (CD4051BD) (para aprovechar el úncio pin analógico) 

# ¿Qué se necesita para correrlo?
El software requiere del circuito conectado a la computadora, junto con python 3 y los módulos: pyserial, numpy y tabulate. 
