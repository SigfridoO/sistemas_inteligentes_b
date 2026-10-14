class Padre:
    def __init__(self):
        print("Soy padre")

    def ensenar(self):
        print("Enseñando...")

class Madre:
    def __init__(self):
        print("Soy madre")

    def cuidar(self):
        print("Cuidando...")

class Hijo(Madre, Padre):
    def __init__(self):
        #super().__init__()
        Padre.__init__(self)
        Madre.__init__(self)
        print("Soy hijo")

def main():
    print("Dentro de main")
    hijo = Hijo()
    hijo.ensenar()
    hijo.cuidar()

if __name__ == "__main__":
    main()