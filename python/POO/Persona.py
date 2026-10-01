
class Persona:
    # constructor
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        print("Dentro del constructor")

    def saludar(self):
        print("====================================================+")
        print(f"Hola mi nombre es {self.nombre} {self.apellido}")

    # to string (represantacion en cadena de caracteres del objeto)
    def __str__(self):
        return ""

def main():
    print("Dentro de main")

    omar = Persona("Omar", "García")
    omar.saludar()

    alejandro = Persona("Alejandro", "Morales")
    alejandro.saludar()

if __name__ == "__main__":
    main()