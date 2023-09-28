from typing import List

import fuzzyfinder

from hotfuzz.item import Item


class Fuzz:

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    def search(self, query: str) -> List[Item]:
        matches = list(fuzzyfinder.fuzzyfinder(query, self.items))
        return matches
