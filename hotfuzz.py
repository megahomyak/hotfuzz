from PyQt6.QtGui import QFont, QFontDatabase, QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import Qt
import sys

class HotFuzz(QMainWindow):
    def __init__(self, screen_size):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        QFontDatabase.addApplicationFont("Fixedsys.ttf")
        font = QFont("Fixedsys Excelsior 3.01", pointSize=30)

        self.prompt = QLabel(self)
        self.prompt.setFont(font)

        self.screen_size = screen_size

        self.set_prompt_text("> ")

    def set_prompt_text(self, text):
        self.prompt.setText(text)

        self.prompt.adjustSize()
        prompt_x = (self.screen_size.width() - self.prompt.width()) // 2
        prompt_y = (self.screen_size.height() - self.prompt.height()) // 10

        self.prompt.move(prompt_x, prompt_y)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 190))
        painter.drawRect(self.rect())

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        character = event.text()
        if character not in ("\n", "\r", ""):
            self.set_prompt_text(self.prompt.text() + character)

app = QApplication(sys.argv)
window = HotFuzz(app.screens()[0].size())
window.showFullScreen()
sys.exit(app.exec())
