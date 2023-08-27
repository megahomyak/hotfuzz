from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import Qt
import sys

class HotFuzz(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 90);")

        QFontDatabase.addApplicationFont("Fixedsys.ttf")
        font = QFont("Fixedsys Excelsior 3.01")

        self.prompt = QLabel(self)
        self.prompt.setFont(font)
        self.prompt.setText("blah")

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()

app = QApplication(sys.argv)
window = HotFuzz()
window.show()
sys.exit(app.exec())
