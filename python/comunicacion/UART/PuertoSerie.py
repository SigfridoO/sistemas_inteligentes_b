import serial

class PuertoSerie:
    def __init__(self, puerto, baudrate):
        self._port = puerto
        self._baudrate = baudrate

        self.puerto_serie = serial.Serial()
        self.puerto_serie.port = self._port #"/dev/ttyUSB0"
        self.puerto_serie.baudrate = self._baudrate      

    def abrir(self):
        self.puerto_serie.baudrate = 115200
        self.puerto_serie.parity = serial.PARITY_NONE
        self.puerto_serie.stopbits = serial.STOPBITS_ONE
        self.puerto_serie.bytesize = serial.EIGHTBITS

        self.puerto_serie.timeout = 1

        self.puerto_serie.open()
        if self.puerto_serie.is_open:
            print(f"Puerto serie {self._port} abierto a {self._baudrate} baudios")

    def cerrar(self):
        if self.puerto_serie.is_open:
            self.puerto_serie.close()
            print(f"Puerto serie {self._port} cerrado")
        

    def escribir(self, data):
        if self.puerto_serie.is_open:
            self.puerto_serie.write(data)
            print(f"Datos enviados: {data}")
        else:
            print("Puerto serie no está abierto. No se pueden enviar datos.")

if puerto_serie.is_open:
    while True:
        res = puerto_serie.read(1)
        if res:
            print("respuesta >> ", ord(res),  res)
