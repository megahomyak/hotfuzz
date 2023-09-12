from PyQt6.QtGui import QFont, QFontDatabase, QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import Qt
import sys
import re

LAST_WORD = re.compile(r"\w+\s*$", flags=re.UNICODE)

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

        self.update_results("")

    def update_results(self, text):
        self.prompt_text = text
        self.prompt.setText("> " + self.prompt_text)

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
        elif event.key() == Qt.Key.Key_Backspace:
            modifiers = QApplication.keyboardModifiers()
            if Qt.KeyboardModifier.ControlModifier in modifiers:
                result = LAST_WORD.sub("", self.prompt_text)
            else:
                result = self.prompt_text[:-1]
            self.update_results(result)
        else:
            character = event.text()
            if character not in ("\n", "\r", ""):
                self.update_results(self.prompt_text + character)

app = QApplication(sys.argv)
window = HotFuzz(app.screens()[0].size())
window.showFullScreen()
sys.exit(app.exec())
