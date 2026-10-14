window+-
+from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        mi_boton = QPushButton("Presioname...")
        # mi_boton.pressed.connect(self.boton_presionado)
        # mi_boton.released.connect(self.boton_liberado)
        # mi_boton.clicked.connect(self.boton_clickeado)
        mi_boton.setCheckable(True)
        mi_boton.clicked.connect(self.boton_con_estado)

        self.setCentralWidget(mi_boton)
        self.resize(200, 100)
        self.setWindowTitle("Mi boton")

    def boton_con_estado(self, valor):
        print(f"El valor es ... {valor}")

    def boton_presionado(self):
        print("Se presiono el boton")

    def boton_liberado(self):
        print("Se libero el boton")

    def boton_clickeado(self):
        print("Se clickeo el boton")

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())