from dataclasses import dataclass
from typing import List, Union


@dataclass
class PlainPart:
    content: str


@dataclass
class HighlightedPart:
    content: str


Part = Union[PlainPart, HighlightedPart]


@dataclass
class Item:
    parts: List[Part]


Index = int
