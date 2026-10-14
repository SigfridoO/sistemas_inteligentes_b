from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
import sys

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.linea_texto = QLineEdit()
        self.linea_texto.setPlaceholderText("Por favor escribe algo...")
        self.linea_texto.textChanged.connect(self.texto_cambiado)
        self.linea_texto.returnPressed.connect(self.texto_retornado)

        self.setCentralWidget(self.linea_texto)
        self.resize(400,80)

    def texto_retornado(self):
        texto = self.linea_texto.text()
        self.setWindowTitle(texto)
        self.linea_texto.clear()

    def texto_cambiado(self):
        texto = self.linea_texto.text()
        print(f"Se escribio >>{texto}")

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())