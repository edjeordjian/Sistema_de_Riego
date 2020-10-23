# Description
The idea was to build a simple and affordable device to water a plant, using sensors to check humidity and light exposure. In addition to the well-known hardware implementation for this purpose, a software control panel was developed in order to inspect the status measured by the sensors, as well as to set the values which are considered acceptable in terms of light and humidity levels. 

# Components
- Arduino ESP8266 (Lolin Nodemcu v3)
- GL5537 photoresistor
- HL-69 humidity sensor
- XJD-33 electrovalve
- SRV-05 relay
- 4051 multiplexor (CD4051BD) (used to take advantage of the only analogic pin available on the board) 

# Circuit
![alt text](media/circuito1.png)

Considering the board's pinout:
![alt text](media/pinout.jpg)

the joins are sketched as follows:
![alt text](media/placa2.png)
![alt text](media/placa1.png)

# Preview
Software control panel:
![alt text](media/menu.png)

Live visualization of light and humidity levels:
![alt text](media/arduino1.gif)

Reducing the light exposure, the electrovalve is activated, letting the water flow.
![alt text](media/arduino2.gif)

# How do I run it?
The control panel can be ran with Python 3, once the device is connected by USB. The following python modules should be installed: pyserial, numpy and tabulate.
