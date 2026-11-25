import argparse
import re
import socket
import threading


class ClienteBluetooth:
    CANAL = 3
    MAX_MENSAJE = 4096

    def __init__(self, direccion, canal=None):
        if not re.fullmatch(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", direccion):
            raise ValueError("La direccion debe tener formato Bluetooth XX:XX:XX:XX:XX:XX")
        self.DIRECCION = direccion
        self.CANAL = self.CANAL if canal is None else canal
        if not 1 <= self.CANAL <= 30:
            raise ValueError("El canal RFCOMM debe estar entre 1 y 30")
        self.cliente = None
        self.buffer = bytearray()
        self.detener = threading.Event()
        self.bloqueo_envio = threading.Lock()
        self.hilo_recepcion = None

    def conectar(self):
        if not hasattr(socket, "AF_BLUETOOTH") or not hasattr(socket, "BTPROTO_RFCOMM"):
            raise RuntimeError("Este Python no dispone de sockets Bluetooth RFCOMM")
        cliente = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        cliente.settimeout(10.0)
        try:
            cliente.connect((self.DIRECCION, self.CANAL))
        except Exception:
            cliente.close()
            raise
        cliente.settimeout(0.5)
        self.cliente = cliente
        self.detener.clear()
        print(f"Conectado a {self.DIRECCION}, canal RFCOMM {self.CANAL}")

    def enviar(self, mensaje):
        if self.cliente is None or self.detener.is_set():
            raise ConnectionError("No existe una conexion Bluetooth activa")
        if "\n" in mensaje or "\r" in mensaje:
            raise ValueError("El mensaje no debe contener saltos de linea")
        datos = mensaje.encode("utf-8")
        if len(datos) > self.MAX_MENSAJE:
            raise ValueError("Mensaje demasiado largo")
        with self.bloqueo_envio:
            self.cliente.sendall(datos + b"\n")

    def recibir(self):
        """Obtiene una linea completa. Conserva la API del cliente original."""
        if self.cliente is None:
            raise ConnectionError("No existe una conexion Bluetooth")
        while not self.detener.is_set():
            if b"\n" in self.buffer:
                indice = self.buffer.index(10)
                if indice > self.MAX_MENSAJE:
                    raise ValueError("Mensaje recibido demasiado largo")
                linea = bytes(self.buffer[:indice]).rstrip(b"\r")
                del self.buffer[:indice + 1]
                return linea.decode("utf-8")
            if len(self.buffer) > self.MAX_MENSAJE:
                raise ValueError("Mensaje recibido demasiado largo")
            try:
                bloque = self.cliente.recv(1024)
            except socket.timeout:
                continue
            if not bloque:
                raise ConnectionError("El servidor cerro la conexion")
            self.buffer.extend(bloque)
        raise ConnectionError("Conexion finalizada")

    def escuchar(self):
        """Recepcion permanente en un hilo; la consola puede enviar a la vez."""
        try:
            while not self.detener.is_set():
                mensaje = self.recibir()
                print(f"\nServidor: {mensaje}")
                if mensaje.lower() == "cerrada":
                    break
        except (OSError, ConnectionError, UnicodeError, ValueError) as error:
            if not self.detener.is_set():
                print(f"\nRecepcion finalizada: {error}")
        finally:
            self.detener.set()

    def desconectar(self):
        self.detener.set()
        if self.cliente is not None:
            try:
                self.cliente.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.cliente.close()
            except OSError:
                pass
            self.cliente = None
        if self.hilo_recepcion is not None and self.hilo_recepcion is not threading.current_thread():
            self.hilo_recepcion.join(timeout=2.0)
        self.buffer.clear()

    def ejecutar(self):
        self.conectar()
        self.hilo_recepcion = threading.Thread(target=self.escuchar, name="RecepcionBluetooth", daemon=True)
        self.hilo_recepcion.start()
        print("Escribe mensajes libremente; 'cerrar' termina la conexion.")
        try:
            while not self.detener.is_set():
                # input() permanece en primer plano; el hilo receptor imprime mensajes entrantes.
                mensaje = input("Cliente> ")
                if self.detener.is_set():
                    break
                self.enviar(mensaje)
                if mensaje.lower() == "cerrar":
                    # Dejar un instante para recibir la confirmacion de cierre del servidor.
                    self.detener.wait(0.5)
                    break
        finally:
            self.desconectar()


def main():
    parser = argparse.ArgumentParser(description="Cliente Bluetooth RFCOMM bidireccional")
    parser.add_argument("--address", required=True, help="MAC Bluetooth del servidor")
    parser.add_argument("--channel", type=int, default=3, help="Canal RFCOMM (predeterminado 3)")
    args = parser.parse_args()
    try:
        ClienteBluetooth(args.address, args.channel).ejecutar()
    except (OSError, RuntimeError, ValueError, ConnectionError, UnicodeError) as error:
        print(f"Error de comunicacion Bluetooth: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nCliente finalizado")


if __name__ == "__main__":
    main()
