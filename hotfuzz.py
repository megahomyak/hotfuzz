from typing import Generic, List, Optional, TypeVar, Union
from PyQt6.QtGui import QFont, QFontDatabase, QFontMetrics, QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QTimer, Qt
import sys
import re
from dataclasses import dataclass
from fuzzyfinder import fuzzyfinder # type: ignore
import enum
import html

LAST_WORD = re.compile(r"\S*\s*$", flags=re.UNICODE)

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

    def get_text(self):
        text = ""
        for part in self.parts:
            text += part.characters
        return text

class HotkeyCollision(Exception):
    def __init__(self, chain):
        self.chain = chain

class EarlyExit(Exception):
    pass

class Mode(enum.Enum):
    HOT = enum.auto()
    FUZZ = enum.auto()

class HotFuzz(QMainWindow):
    def __init__(self, screen_size, options, output_buffer):
        super().__init__()

        self.setCursor(Qt.CursorShape.BlankCursor)

        self.prompt_text = ""

        self.output_buffer = output_buffer
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
                        character = character.lower()
                        chain.append(character)
                        if "end" in base_dict:
                            raise HotkeyCollision(chain)
                        elif character not in base_dict:
                            base_dict[character] = {}
                        base_dict = base_dict[character]
            if highlighted:
                base_dict["end"] = option

        self.options_fuzzy = options

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        QFontDatabase.addApplicationFont("Fixedsys.ttf")
        font = QFont("Fixedsys Excelsior 3.01", pointSize=30)
        font_metrics = QFontMetrics(font)

        self.mode_label = QLabel(self)
        self.mode_label.setFont(font)
        self.mode_label.move(0, 0)

        self.prompt = QLabel(self)
        self.prompt.setFont(font)
        self.prompt.setStyleSheet("color: #00FF00;")
        self.prompt.setTextFormat(Qt.TextFormat.PlainText)

        self.hint = QLabel(self)
        self.hint.setFont(font)
        self.hint.setText("use / to switch modes")
        self.hint.adjustSize()
        self.hint.move(self.screen_size.width() - self.hint.width(), 0)

        self.prompt_y = (self.screen_size.height() - self.prompt.height()) // 10
        self.prompt_x = self.screen_size.width() // 3

        output_x = self.screen_size.width() // 5

        self.output = QLabel(self)
        self.output.setFont(font)

        output_y = self.prompt_y + font_metrics.height() * 2
        self.output.move(output_x, output_y)

        self.set_mode(Mode.HOT)

        self.prompt_cursor = " "

        def blink():
            if self.prompt_cursor == "_":
                self.prompt_cursor = " "
            elif self.prompt_cursor == " ":
                self.prompt_cursor = "_"
            self.redraw_prompt()

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(blink)
        self.blink_timer.start(500)

        self.show_results()

    def set_mode(self, mode):
        self.mode = mode
        if mode == Mode.FUZZ:
            self.mode_label.setText("[FUZZ]")
        elif mode == Mode.HOT:
            self.mode_label.setText("[HOT]")
        self.mode_label.adjustSize()
        self.redraw_output()

    def get_results_fuzz(self, text):
        results = fuzzyfinder(text, self.options_fuzzy, accessor=Option.get_text)
        return results

    def get_results_hot(self, text):
        base_dict = self.options_hotkeys
        for character in text:
            try:
                base_dict = base_dict[character]
            except KeyError:
                return []
        try:
            result = base_dict["end"]
        except KeyError:
            results = []
            remaining = [base_dict]
            while remaining:
                base_dict = remaining.pop()
                try:
                    results.append(base_dict["end"])
                except KeyError:
                    pass
                for key, value in base_dict.items():
                    if key != "end":
                        remaining.append(value)
            return results
        else:
            self.output_buffer[0] = result
            self.close()
            raise EarlyExit

    def redraw_prompt(self):
        self.prompt.setText("> " + self.prompt_text + self.prompt_cursor)
        self.prompt.adjustSize()

        x = (self.screen_size.width() - self.prompt.width()) // 2
        self.prompt.move(x, self.prompt_y)

    def show_results(self):
        self.redraw_prompt()
        self.redraw_output()

    def redraw_output(self):
        if self.mode == Mode.FUZZ:
            results = self.get_results_fuzz(self.prompt_text)
        elif self.mode == Mode.HOT:
            try:
                results = self.get_results_hot(self.prompt_text)
            except EarlyExit:
                return
        lines = []
        for option in results: # type: ignore
            line = ""
            for part in option.parts:
                if isinstance(part, HighlightedPart):
                    line += "<span style='color: #00FF00;'>"
                    line += html.escape(part.characters)
                    line += "</span>"
                elif isinstance(part, PlainPart):
                    line += html.escape(part.characters)
            lines.append(line)
        self.output.setText("<br>".join(lines))
        self.output.adjustSize()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 210))
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
            if character == "/":
                if self.mode == Mode.FUZZ:
                    self.set_mode(Mode.HOT)
                elif self.mode == Mode.HOT:
                    self.set_mode(Mode.FUZZ)
            elif character not in ("\n", "\r", ""):
                self.prompt_text += character.lower()
                self.show_results()

def run(options: List[Option[T]]) -> Optional[Option[T]]:
    output_buffer = [None]
    app = QApplication(sys.argv)
    window = HotFuzz(app.screens()[0].size(), options, output_buffer)
    window.showFullScreen()
    app.exec()
    return output_buffer[0]
