from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

import sys
from pathlib import Path

def abs_path(nombre):
    return str(Path(__file__).parent.absolute() / nombre)

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        mi_etiqueta = QLabel("Bienvenido")
        mi_etiqueta.setAlignment(Qt.AlignmentFlag.AlignRight | 
                                 Qt.AlignmentFlag.AlignVCenter)

        fuente = QFont("Manjari", 20, QFont.Weight.Bold)
        mi_etiqueta.setFont(fuente)
        ruta = abs_path("gato.jpeg")
        print (ruta)
        imagen = QPixmap(ruta)
        mi_etiqueta.setPixmap(imagen)
        mi_etiqueta.setScaledContents(True)
        
 
        self.setCentralWidget(mi_etiqueta)
        self.resize(300,80)
        

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())