/* MANEJO DE HARDWARE */
#define PIN_ANALOGICO A0
#define PIN_MUX 10
#define PIN_RELE 5
#define BAUD_RATE 9600
#define DESACTIVADO LOW
#define ACTIVADO HIGH

/* CONTROL DE RIEGO */
#define INTERVALO_RELE 500
int intervalo_consulta_sensores =  1000;
int limite_de_luz =  300;
int limite_de_humedad = 800;

String estado;
String temp;

/* Setup se ejecuta una sola vez, y loop permanentemente */
void setup() {
  /* Entradas */
  pinMode(PIN_ANALOGICO, INPUT);
  
  /* Salidas */
  pinMode(PIN_MUX, OUTPUT);
  pinMode(PIN_RELE, OUTPUT);
  
  digitalWrite(PIN_MUX, LOW); /* Las lecturas analógicas iniciales son de humedad */
  digitalWrite(PIN_RELE, DESACTIVADO); /* La electroválvula inicia apagada */
  Serial.begin(BAUD_RATE); /* Iniciar transmisión bilateral con placa */

  estado = 'n';
  /* n: Normal, abre la valvula dependiendo del estado de los sensores
   * a: Abierta, independientemente del estado de los sensores 
   * c: Cerrada, idem anterior.
   */
}

void loop() {
  delay(intervalo_consulta_sensores);  /* Pausar el procesador del arduino. */
  
  /* Lectura de humedad en una cantidad fija de bytes*/
  float humedad = analogRead(PIN_ANALOGICO);
  char hum[8]; 
  sprintf(hum, "%07.2f", humedad);
  //Serial.println( humedad ); 

  /* Las lecturas analógicas ahora son de luz */
  digitalWrite(PIN_MUX, HIGH); 
  delay(INTERVALO_RELE);
    
  /* Lectura de luz en una cantidad fija de bytes */
  float luz = analogRead(PIN_ANALOGICO);
  char luu[8];
  sprintf(luu, "%07.2f", luz); 
    
  /*Enviar información sobre luz y humedad*/
  Serial.print("Humedad: ");
  Serial.print(hum);
  Serial.print(" ");
  Serial.print("Luz: "); 
  Serial.print(luu);
  Serial.print(" ");

  if (Serial.available() > 0) {
    temp = Serial.readString();
    
    if (temp.startsWith("h")) {
      limite_de_humedad = temp.substring(1).toInt();
    }
    
    else if (temp.startsWith("l")) {
      limite_de_luz = temp.substring(1).toInt();
    }

    else if (temp.startsWith("i")) {
      intervalo_consulta_sensores = temp.substring(1).toInt()*1000;
    }
    
    else if (temp.startsWith("m")) {
      int comienzo_luz = temp.indexOf('l');
      limite_de_humedad = temp.substring(1,comienzo_luz).toInt();
      limite_de_luz = temp.substring(comienzo_luz+1).toInt();
    }
    
    else {
      estado = temp;  
    }
  }

  if (estado == "n") {
    /* Condición de riego: de noche, y cuando no está mojada la tierra */
    if ( ( humedad > limite_de_humedad ) && 
         ( luz < limite_de_luz ) ){
      digitalWrite(PIN_RELE, ACTIVADO); /* Accionar relé que activa la electroválvula */
    } 
      
    else {
      digitalWrite(PIN_RELE, DESACTIVADO); /* Desactivar el relé */
    }
  }
  
  else if (estado == "a"){
    digitalWrite(PIN_RELE, ACTIVADO);
  }

  else if(estado == "c") {
    digitalWrite(PIN_RELE, DESACTIVADO);  
  }
  
  digitalWrite(PIN_MUX, LOW); /*Las lecturas analógicas vuelven a ser de humedad*/
  Serial.println(digitalRead(PIN_RELE));  
}
