import argparse
import socket
import threading


class ServidorBluetooth:
    CANAL = 3
    MAX_MENSAJE = 4096

    def __init__(self, canal=None):
        self.CANAL = self.CANAL if canal is None else canal
        if not 1 <= self.CANAL <= 30:
            raise ValueError("El canal RFCOMM debe estar entre 1 y 30")
        self.servidor = None
        self.clientes = {}  # ID numerico -> (socket, direccion)
        self.hilos = set()
        self.bloqueos_envio = {}  # ID -> Lock; serializa las respuestas y la consola
        self.siguiente_id = 1
        self.bloqueo = threading.Lock()
        self.detener = threading.Event()

    def obtener_clientes(self):
        with self.bloqueo:
            return [(identificador, direccion) for identificador, (_, direccion) in self.clientes.items()]

    def enviar_cliente(self, identificador, mensaje):
        if "\n" in mensaje or "\r" in mensaje:
            raise ValueError("El mensaje no debe contener saltos de linea")
        datos = mensaje.encode("utf-8")
        if len(datos) > self.MAX_MENSAJE:
            raise ValueError("Mensaje demasiado largo")
        with self.bloqueo:
            sesion = self.clientes.get(identificador)
            bloqueo_envio = self.bloqueos_envio.get(identificador)
        if sesion is None or bloqueo_envio is None:
            return False
        try:
            with bloqueo_envio:
                sesion[0].sendall(datos + b"\n")
            return True
        except OSError:
            return False

    def enviar_todos(self, mensaje):
        with self.bloqueo:
            ids = list(self.clientes)
        return sum(self.enviar_cliente(identificador, mensaje) for identificador in ids)

    def procesar_mensaje(self, mensaje, direccion):
        print(f"\n[{direccion[0]}] Recibido: {mensaje}")
        if mensaje.lower() == "cerrar":
            return "cerrada"
        # Se mantiene la respuesta del protocolo original.
        return "aceptada"

    def atender_cliente(self, cliente_socket, direccion, identificador=None):
        if identificador is None:
            with self.bloqueo:
                identificador = self.siguiente_id
                self.siguiente_id += 1
                self.clientes[identificador] = (cliente_socket, direccion)
                self.bloqueos_envio[identificador] = threading.Lock()
        print(f"\nCliente {identificador} conectado: {direccion}")
        buffer = bytearray()
        try:
            cliente_socket.settimeout(0.5)
            while not self.detener.is_set():
                try:
                    bloque = cliente_socket.recv(1024)
                except socket.timeout:
                    continue
                except OSError:
                    break
                if not bloque:
                    break
                buffer.extend(bloque)
                while b"\n" in buffer:
                    indice = buffer.index(10)
                    if indice > self.MAX_MENSAJE:
                        self.enviar_cliente(identificador, "error: mensaje demasiado largo")
                        return
                    linea = bytes(buffer[:indice]).rstrip(b"\r")
                    del buffer[:indice + 1]
                    try:
                        mensaje = linea.decode("utf-8")
                    except UnicodeDecodeError:
                        self.enviar_cliente(identificador, "error: UTF-8 invalido")
                        continue
                    try:
                        respuesta = self.procesar_mensaje(mensaje, direccion)
                    except Exception as error:
                        print(f"Error procesando mensaje del cliente {identificador}: {error}")
                        self.enviar_cliente(identificador, "error: procesamiento fallido")
                        continue
                    if respuesta is not None:
                        self.enviar_cliente(identificador, respuesta)
                    if respuesta == "cerrada":
                        return
                if len(buffer) > self.MAX_MENSAJE:
                    self.enviar_cliente(identificador, "error: mensaje demasiado largo")
                    return
        finally:
            with self.bloqueo:
                self.clientes.pop(identificador, None)
                self.bloqueos_envio.pop(identificador, None)
                self.hilos.discard(threading.current_thread())
            try:
                cliente_socket.close()
            except OSError:
                pass
            print(f"\nCliente {identificador} desconectado: {direccion}")

    def consola(self):
        print("Comandos: /clientes, /enviar ID mensaje, /todos mensaje, /salir.")
        print("Escribir texto sin comando lo envia a todos los clientes.")
        try:
            while not self.detener.is_set():
                entrada = input("Servidor> ").strip()
                if not entrada:
                    continue
                if entrada == "/salir":
                    self.cerrar()
                    break
                if entrada == "/clientes":
                    clientes = self.obtener_clientes()
                    if not clientes:
                        print("No hay clientes conectados")
                    for identificador, direccion in clientes:
                        print(f"Cliente {identificador}: {direccion[0]}")
                    continue
                if entrada.startswith("/enviar "):
                    partes = entrada.split(" ", 2)
                    if len(partes) != 3 or not partes[1].isdigit():
                        print("Uso: /enviar ID mensaje")
                        continue
                    if not self.enviar_cliente(int(partes[1]), partes[2]):
                        print("No se pudo enviar: cliente inexistente o desconectado")
                    continue
                if entrada.startswith("/todos "):
                    mensaje = entrada[len("/todos "):]
                else:
                    mensaje = entrada
                try:
                    print(f"Enviado a {self.enviar_todos(mensaje)} cliente(s)")
                except ValueError as error:
                    print(f"Error: {error}")
        except (KeyboardInterrupt, EOFError):
            self.cerrar()

    def iniciar(self, consola=True):
        if not hasattr(socket, "AF_BLUETOOTH") or not hasattr(socket, "BTPROTO_RFCOMM"):
            raise RuntimeError("Este Python no dispone de sockets Bluetooth RFCOMM")
        self.detener.clear()
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as servidor:
            self.servidor = servidor
            servidor.bind(("00:00:00:00:00:00", self.CANAL))
            servidor.listen(5)
            servidor.settimeout(0.5)
            print(f"Servidor Bluetooth RFCOMM escuchando en canal {self.CANAL}")
            hilo_consola = None
            if consola:
                hilo_consola = threading.Thread(target=self.consola, name="ConsolaBluetooth", daemon=True)
                hilo_consola.start()
            try:
                while not self.detener.is_set():
                    try:
                        cliente_socket, direccion = servidor.accept()
                    except socket.timeout:
                        continue
                    except OSError:
                        if self.detener.is_set():
                            break
                        raise
                    with self.bloqueo:
                        identificador = self.siguiente_id
                        self.siguiente_id += 1
                        self.clientes[identificador] = (cliente_socket, direccion)
                        self.bloqueos_envio[identificador] = threading.Lock()
                    hilo = threading.Thread(
                        target=self.atender_cliente,
                        args=(cliente_socket, direccion, identificador),
                        name=f"Bluetooth-{identificador}",
                        daemon=True,
                    )
                    with self.bloqueo:
                        self.hilos.add(hilo)
                    hilo.start()
            except KeyboardInterrupt:
                print("\nDeteniendo servidor Bluetooth...")
            finally:
                self.detener.set()
                with self.bloqueo:
                    clientes = [sesion[0] for sesion in self.clientes.values()]
                    hilos = list(self.hilos)
                for cliente in clientes:
                    try:
                        cliente.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    try:
                        cliente.close()
                    except OSError:
                        pass
                for hilo in hilos:
                    hilo.join(timeout=2.0)
                self.servidor = None
                print("Servidor Bluetooth cerrado")

    def cerrar(self):
        self.detener.set()
        if self.servidor is not None:
            try:
                self.servidor.close()
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description="Servidor Bluetooth RFCOMM bidireccional y multicliente")
    parser.add_argument("--channel", type=int, default=3, help="Canal RFCOMM (predeterminado 3)")
    args = parser.parse_args()
    try:
        ServidorBluetooth(args.channel).iniciar()
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error al iniciar Bluetooth: {error}")


if __name__ == "__main__":
    main()
