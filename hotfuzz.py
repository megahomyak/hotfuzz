from typing import Generic, List, TypeVar, Union
from PyQt6.QtGui import QFont, QFontDatabase, QFontMetrics, QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import Qt
import sys
import re
from dataclasses import dataclass
from fuzzyfinder import fuzzyfinder # type: ignore
import enum

LAST_WORD = re.compile(r"\w+\s*$", flags=re.UNICODE)

@dataclass
class HighlightedPart:
    characters: str

@dataclass
class PlainPart:
    characters: str

OptionPart = Union[PlainPart, HighlightedPart]

T = TypeVar("T")

@dataclass
class Option(Generic[T]):
    parts: List[OptionPart]
    payload: T

    def get_plain_text(self):
        text = ""
        for part in self.parts:
            if isinstance(part, PlainPart):
                text += part.characters
        return text

class HotkeyCollision(Exception):
    def __init__(self, chain):
        self.chain = chain

class Mode(enum.Enum):
    HOT = enum.auto()
    FUZZ = enum.auto()

class HotFuzz(QMainWindow):
    def __init__(self, screen_size, options, output_buffer):
        super().__init__()

        self.screen_size = screen_size
        self.options_hotkeys = {}
        for option in options:
            base_dict = self.options_hotkeys
            chain = []
            highlighted = False
            for part in option.parts:
                if isinstance(part, HighlightedPart):
                    highlighted = True
                    for character in part.characters:
                        chain.append(character)
                        if character in base_dict:
                            raise HotkeyCollision(chain)
                        else:
                            base_dict[character] = {}
                            base_dict = base_dict[character]
            if highlighted:
                base_dict["end"] = option

        self.options_fuzzy = options

        self.output_buffer = output_buffer

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        QFontDatabase.addApplicationFont("Fixedsys.ttf")
        font = lambda size: QFont("Fixedsys Excelsior 3.01", pointSize=size)
        font_metrics = QFontMetrics(font(30))

        self.current_mode = QLabel(self)
        self.current_mode.setFont(font(20))
        self.current_mode.move(0, 0)
        self.current_mode.setText("[MODE]")

        self.prompt = QLabel(self)
        self.prompt.setFont(font(30))
        self.prompt.setStyleSheet("color: #00FF00;")
        self.prompt.setTextFormat(Qt.TextFormat.PlainText)

        self.prompt_y = (self.screen_size.height() - self.prompt.height()) // 10

        self.output = QLabel(self)
        self.output.setFont(font(30))

        output_x = (self.screen_size.width() - self.output.width()) // 5
        output_y = self.prompt_y + font_metrics.height() * 3
        self.output.setText("abc")
        self.output.move(output_x, output_y)

        self.prompt_text = ""
        self.show_results()

    def get_results_fuzzy(self, text):
        results = fuzzyfinder(text, self.options_fuzzy, accessor=Option.get_plain_text)
        return results

    def get_results_hot(self, text):
        pass # TODO

    def show_results(self):
        if self.prompt_text:
            self.prompt.setText("> " + self.prompt_text)
        else:
            self.prompt.setText(">")

        self.prompt.adjustSize()
        prompt_x = (self.screen_size.width() - self.prompt.width()) // 2

        self.prompt.move(prompt_x, self.prompt_y)

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
                self.prompt_text = LAST_WORD.sub("", self.prompt_text)
            else:
                self.prompt_text = self.prompt_text[:-1]
            self.show_results()
        else:
            character = event.text()
            if character not in ("\n", "\r", ""):
                self.prompt_text += character
                self.show_results()

def run(options):
    output_buffer = [None]
    app = QApplication(sys.argv)
    window = HotFuzz(app.screens()[0].size(), options, output_buffer)
    window.showFullScreen()
    app.exec()
