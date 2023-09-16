from abc import ABC, abstractmethod
from typing import Iterable, Union
from dataclasses import dataclass

@dataclass
class HighlightedPart:
    characters: str

@dataclass
class PlainPart:
    characters: str

Part = Union[PlainPart, HighlightedPart]

class Item(ABC):

    @abstractmethod
    def get_parts(self) -> Iterable[Part]:

