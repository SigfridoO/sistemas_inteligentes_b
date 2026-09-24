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
TON[0].tiempo = (unsigned long) 10000;
Serial.begin(115200);

}

void loop() {

TON[0].entrada = 1;    // Señal de entrada al TON
actualizarTON(0);
Serial.printf("\nentrada %d     salida %d   tiempo actual %d", TON[0].entrada, TON[0].salida, TON[0].tiempoActual);
}




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
