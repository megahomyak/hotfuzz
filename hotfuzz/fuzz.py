from typing import List
import difflib

from hotfuzz.item import Item, ItemIndex


def diff(string_a, string_b):
    return difflib.SequenceMatcher(None, string_a.casefold(), string_b.casefold()).ratio()


class Fuzz:

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    def search(self, query: str) -> List[ItemIndex]:
        if not query:
            return list(range(len(self.items)))
        matches = [
            (item_index, diff(query, item))
            for item_index, item
            in enumerate(self.items)
        ]
        matches = list(filter(lambda pair: pair[1] > 0.2, matches))
        matches.sort(key=lambda pair: pair[1], reverse=True)
        return list(map(lambda pair: pair[0], matches))
