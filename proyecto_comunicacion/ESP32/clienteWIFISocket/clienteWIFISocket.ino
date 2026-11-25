#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "ardilluda2";
const char* password = "01971101";
const char* server_ip = "192.168.0.106";
const uint16_t server_port = 65432;

WiFiClient cliente;
uint8_t contador = 0;

#define NUMERO_DE_M 8
uint8_t M[NUMERO_DE_M] = {0};

unsigned long tiempoReconexion = 0;
const unsigned long intervaloReconexion = 3000;

//////////////////////////////////////////////// Temporizadores

#define  numeroDeTON 16

struct temporizador {
    byte entrada;
    byte salida;
    unsigned long tiempo;
    unsigned long tiempoActual;
} TON[numeroDeTON];

struct temporizadorAux {
    byte bandera;
    unsigned long tiempo_Aux1;
    unsigned long tiempo_Aux2;
} TON_Aux[numeroDeTON];

void actualizarTON (int);

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando cliente WIFI en ESP32");

  TON[0].tiempo = 1000;
  TON[0].entrada = false;

  TON[1].tiempo = 3000;

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
}

void loop() {

  M[0] =  WiFi.status() == WL_CONNECTED;

  M[1] = M[0] && cliente.connected();

  // Temporizador para el envio de datos
  TON[0].entrada = M[1] && !M[2];
  actualizarTON(0);

  M[2] = TON[0].salida;

  // Temporizador de reconexión
  TON[1].entrada = !M[1] && !M[3];
  actualizarTON(1);

  M[3] = TON[1].salida;

  // TODO: REconexion:
  //////
  if (M[3]){
     if (!M[0]) {
      Serial.println("Reconectando Wifi...");
      WiFi.reconnect();
     } else {
      Serial.print("Conectando al servidor");
      Serial.print(server_ip);
      Serial.print(":");
      Serial.println(server_port);

      cliente.stop();
      if (cliente.connect(server_ip, server_port)){
        Serial.println("Conexción establecida");
        Serial.print("IP Local: ");
        Serial.println(WiFi.localIP());
      } else {
        Serial.println("No se pudo conectar al servidor");
      }
     }
  }
  // Enviar un byte
  if (M[2]) {
      uint8_t dato = contador;
      if (cliente.write(&dato, 1) == 1) {
        cliente.write('\n');
        Serial.print("Byte enviado");
        Serial.println(dato);

        contador++;
      } else {
        Serial.println("Error al enviar el byte");
        cliente.stop();
      }
  }
  delay(1); // Para darle estabilida al microcontrolador


  //Serial.printf("\nM[0]= %d, M[1]= %d", M[0], M[1]);
  /*
  if () {
      TON[0].entrada = false;
      actualizarTON(0);

      TON[1].entrada = !TON[1].salida;
      actualizarTON(1);

      if (TON[1].salida) {
          Serial.print("Reconectando WiFi... ");
          WiFi.reconnect();
     }
    return;
  } else {
    Serial.println("WIfi conectado");
  }
*/
}






//////////////////////////////////////////////// Temporizadores


void actualizarTON (int i) {
     if (TON [i].entrada)
   {
        if (!TON_Aux[i].bandera) {
           TON_Aux[i].bandera = true;
           TON_Aux[i].tiempo_Aux1 = millis ();  
        }
        TON_Aux[i].tiempo_Aux2 = millis ();
        TON [i].tiempoActual = TON_Aux[i].tiempo_Aux2 - TON_Aux[i].tiempo_Aux1;

        if (TON [i].tiempoActual > TON [i].tiempo) {
            TON [i].salida = true;
        }
    } else {
        TON [i].salida = false;
        TON_Aux[i].bandera = false;
    }
}
