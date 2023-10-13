from typing import List, Optional
import typing
import html
import math
import re

from PyQt6.QtCore import QSize, QTimer, Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QPainter
from hotfuzz.mode import Mode
from hotfuzz.item import ItemIndex
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

if typing.TYPE_CHECKING:
    from .hotfuzz import HotFuzz


LAST_WORD = re.compile(r"\S*\s*$", flags=re.UNICODE)


class EarlyExit(Exception):
    pass


class Window(QMainWindow):

    def __init__(self, hotfuzz: "HotFuzz", screen_size: QSize):
        super().__init__()
        self.hotfuzz = hotfuzz
        self.output: Optional[ItemIndex] = None

        self.setCursor(Qt.CursorShape.BlankCursor)

        self.prompt_text = ""
        self.prompt_cursor = ""

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        QFontDatabase.addApplicationFont("Fixedsys.ttf")
        font = QFont("Fixedsys Excelsior 3.01", pointSize=30)

        aspect_ratio = 4/3

        if screen_size.width() > screen_size.height() * aspect_ratio:
            height = screen_size.height()
            width = int(height * aspect_ratio)
        else:
            width = screen_size.width()
            height = int(width * (aspect_ratio ** -1))

        # QFontMetrics are broken and return incorrect values for character width and height
        char_width = 20
        char_height = 40
        self.chars_amount_vertical = height // char_height
        self.chars_amount_horizontal = width // char_width
        width = self.chars_amount_horizontal * char_width
        height = self.chars_amount_vertical * char_height

        self.items_list_size = self.chars_amount_vertical - 4 # 6 other GUI lines
        self.items_list_center_index = math.ceil(self.items_list_size / 2) - 1

        x = (screen_size.width() - width) // 2
        y = (screen_size.height() - height) // 2

        self.text = QLabel(self)
        self.text.setFont(font)
        self.text.setTextFormat(Qt.TextFormat.RichText)
        self.text.move(x, y)
        self.text.setMinimumSize(width, height)
        self.text.setAlignment(Qt.AlignmentFlag.AlignTop)

        def blink():
            if self.prompt_cursor == "_":
                self.prompt_cursor = ""
            elif self.prompt_cursor == "":
                self.prompt_cursor = "_"
            self.redraw_text()

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(blink)
        self.blink_timer.start(500)

        self.results: List[ItemIndex] = None # type: ignore
        self.selection_index = 0
        self.show_results()

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
            try:
                self.show_results()
            except EarlyExit:
                pass
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            try:
                result = self.results[self.selection_index]
            except IndexError:
                pass
            else:
                self.finish(result)
        elif event.key() == Qt.Key.Key_Up:
            if self.selection_index != 0:
                self.selection_index -= 1
                self.redraw_text()
        elif event.key() == Qt.Key.Key_Down:
            if self.selection_index != len(self.results) - 1:
                self.selection_index += 1
                self.redraw_text()
        else:
            character = event.text()
            if character == "/":
                if self.hotfuzz.mode == Mode.FUZZ:
                    self.hotfuzz.mode = Mode.HOT
                elif self.hotfuzz.mode == Mode.HOT:
                    self.hotfuzz.mode = Mode.FUZZ
                self.prompt_text = ""
                self.show_results()
            elif character not in ("\n", "\r", ""):
                if self.hotfuzz.mode == Mode.FUZZ:
                    self.prompt_text += character
                elif self.hotfuzz.mode == Mode.HOT:
                    self.prompt_text += character.upper()
                try:
                    self.show_results()
                except EarlyExit:
                    pass

    def finish(self, output: ItemIndex):
        self.output = output
        self.close()

    def show_results(self):
        if self.hotfuzz.initially_invisible:
            if self.prompt_text == "" and self.hotfuzz.mode == Mode.HOT:
                self.setWindowOpacity(0)
            else:
                self.setWindowOpacity(1)

        if self.hotfuzz.mode == Mode.FUZZ:
            results = self.hotfuzz.fuzz.search(self.prompt_text)
        else:
            result = self.hotfuzz.hot.search(self.prompt_text)
            if result is None:
                results = []
            elif isinstance(result, list):
                results = result
            else:
                self.finish(result)
                raise EarlyExit()
        self.selection_index = 0
        self.results = results
        self.redraw_text()

    def redraw_text(self):
        text = ""

        if self.hotfuzz.mode == Mode.HOT:
            mode = "[HOT]"
        elif self.hotfuzz.mode == Mode.FUZZ:
            mode = "[FUZZ]"

        beginning_index = max(
            min(
                self.selection_index - self.items_list_center_index,
                len(self.results) - self.items_list_size
            ),
            0
        )
        end_index = beginning_index + self.items_list_size
        items_view = self.results[beginning_index:end_index]
        biased_selection_index = self.selection_index - beginning_index

        results_as_strings = []
        for view_item_index, item_index in enumerate(items_view):
            item = self.hotfuzz.items[item_index]
            item = html.escape(item)
            if view_item_index == biased_selection_index:
                results_as_strings.append(
                    f"&nbsp;&nbsp;<span style='color: #000000; background-color: #FFFFFF'>{item}</span>"
                )
            else:
                results_as_strings.append(f"&nbsp;&nbsp;{item}")

        if len(self.results) == 1:
            matched_records_text = "1 record matched"
        else:
            matched_records_text = f"{len(self.results)} records matched"

        upper_spaces_amount = self.chars_amount_horizontal - len(mode) - len(matched_records_text)

        text += mode + ("&nbsp;" * upper_spaces_amount) + matched_records_text
        text += "<br/><br/>"
        text += "&nbsp;>&nbsp;" + self.prompt_text + self.prompt_cursor
        text += "<br/><br/>"
        text += "<br/>".join(results_as_strings)

        self.text.setText(text)
