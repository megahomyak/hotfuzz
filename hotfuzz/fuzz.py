from typing import List

from hotfuzz.item import Item, ItemIndex

from fuzzyfinder import fuzzyfinder


class Fuzz:

    def __init__(self, items: List[Item]) -> None:
        self.items = list(enumerate(items))

    def search(self, query: str) -> List[ItemIndex]:
        if not query:
            return list(range(len(self.items)))
        matches = fuzzyfinder(
            query,
            self.items,
            accessor=lambda pair: pair[1],
        )
        return list(map(lambda pair: pair[0], matches))
