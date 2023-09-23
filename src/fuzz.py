from typing import Iterable, List
from .item import HighlightedPart, Item, PlainPart
from . import item


class Fuzz:
    def __init__(self, items: List[Item]):
        processed_items = []
        for item in items:
            item_text = ""
            for part in item.parts:
                if isinstance(part, HighlightedPart):
                    item_text += part.content
                elif isinstance(part, PlainPart):
                    item_text += part.content
            processed_items.append(item_text)
        self.items = processed_items

    def filter(self, query: str) -> Iterable[item.Index]:
        matches = []
        for index, item_text in enumerate(self.items):
