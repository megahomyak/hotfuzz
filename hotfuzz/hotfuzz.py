from typing import List, Optional

from PyQt6.QtWidgets import QApplication
from hotfuzz.fuzz import Fuzz

from .hot import Hot
from .mode import Mode

from .item import Item
from .window import Window

app = None

class HotFuzz:

    def __init__(self, items: List[Item]):
        self.hot = Hot(items)
        self.fuzz = Fuzz(items)
        self.mode = Mode.HOT

    def run(self) -> Optional[Item]:
        global app
        if app is None:
            app = QApplication([])
        window = Window(self, app.primaryScreen().size())
        window.showFullScreen()
        app.exec()
        return window.output