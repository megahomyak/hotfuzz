from typing import List, Optional

from PyQt6.QtWidgets import QApplication
from hotfuzz.fuzz import Fuzz

from .hot import Hot
from .mode import Mode

from .item import Item, ItemIndex
from .window import Window

app = None

class HotFuzz:

    def __init__(self, items: List[Item], *, initially_invisible: bool):
        self.hot = Hot(items)
        self.fuzz = Fuzz(items)
        self.mode = Mode.HOT
        self.items = items
        self.initially_invisible = initially_invisible

    def run(self) -> Optional[ItemIndex]:
        global app
        if app is None:
            app = QApplication([])
        window = Window(self, app.primaryScreen().size())
        window.showFullScreen()
        app.exec()
        return window.output
