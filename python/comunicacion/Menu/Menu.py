import sys
from pathlib import Path

from InquirerPy import inquirer
from blessed import Terminal

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from UART.PuertoSerie import PuertoSerie

term = Terminal()

class Menu:

    def __init__(self):
        self.puerto_serie = PuertoSerie("/dev/ttyUSB0", 115200)

    def pausa(self):
        input(f"{term.yellow}Presione Enter para continuar...{term.normal}")

    def limpiar_pantalla(self):
        print(f"{term.home + term.clear}")

    def submenu_puerto_serie(self):
        while True:
            self.limpiar_pantalla()
            print(f"{term.orange}=======================================")
            print(f"{term.cyan3}Puerto Serie - Submenú")
            print(f"{term.orange}======================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción del puerto serie:",
                choices=[
                    {"name": "1. Abrir puerto serie", "value": "puerto_serie_abrir"},
                    {"name": "2. Cerrar puerto serie", "value": "puerto_serie_cerrar"},
                    {"name": "3. Volver al menú principal", "value": "volver"},
                ]
            ).execute()

            match opcion:
                case "puerto_serie_abrir":
                    self.puerto_serie.abrir()

                case "puerto_serie_cerrar":
                    self.puerto_serie.cerrar()
                    
                case "volver":
                    print("Volviendo al menú principal...")
                    break
                case _:
                    print("Opción no válida. Intente nuevamente.")
            self.pausa()

    def submenu_senales_digitales(self):
        while True:
            self.limpiar_pantalla()
            print(f"{term.orange}=======================================")
            print(f"{term.cyan3}Señales Digitales - Submenú")
            print(f"{term.orange}======================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción de señales digitales:",
                choices=[
                    {"name": "1. Prender led", "value": "PRENDER_LED"},
                    {"name": "2. Apagar led", "value": "APAGAR_LED"},
                    {"name": "3. Volver al menú principal", "value": "volver"},
                ]
            ).execute()

            match opcion:
                case "PRENDER_LED":
                    print("Opción seleccionada: Prender led")
                    if not self.puerto_serie.puerto_serie.is_open:
                        print("El puerto serie no está abierto. Por favor, abra el puerto serie primero.")  
                        return
                    arreglo_bytes = bytearray(100)
                    arreglo_bytes[:6] = b'?0121*'
                    self.puerto_serie.escribir(arreglo_bytes[:6])

                case "APAGAR_LED":
                    print("Opción seleccionada: Apagar led")
                    if not self.puerto_serie.puerto_serie.is_open:
                        print("El puerto serie no está abierto. Por favor, abra el puerto serie primero.")  
                        return
                    arreglo_bytes = bytearray(100)
                    arreglo_bytes[:6] = b'?0131*'
                    self.puerto_serie.escribir(arreglo_bytes[:6])

                    
                case "volver":
                    print("Volviendo al menú principal...")
                    break
                case _:
                    print("Opción no válida. Intente nuevamente.")
            self.pausa()


    def mostrar_menu(self):
        while True:
            self.limpiar_pantalla()

            print(f"{term.orange}=======================================")
            print(f"{term.cyan3}Bienvenido al menú de opciones")
            print(f"{term.orange}======================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "1. Puerto serie", "value": "PUERTO_SERIE"},
                    {"name": "2. Señales digitales", "value": "SENALES_DIGITALES"},
                    {"name": "3. Cerrar puerto serie", "value": "puerto_serie_cerrar"},
                    {"name": "4. Salir", "value": "salir"},
                ]
            ).execute()

            match opcion:
                case "PUERTO_SERIE":
                    self.submenu_puerto_serie()

                case "SENALES_DIGITALES":
                    self.submenu_senales_digitales()

                case "puerto_serie_cerrar":
                    print("Opción seleccionada: Cerrar puerto serie")
                    
                case "salir":
                    print("Saliendo del programa...")
                    sys.exit(0)
                case _:
                    print("Opción no válida. Intente nuevamente.")
            # self.pausa()


def main():
    

    menu = Menu()
    try:
        menu.mostrar_menu()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario. Saliendo...")
        
if __name__ == "__main__":
    main()