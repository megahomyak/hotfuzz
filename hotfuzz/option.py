from typing import Generic, List, TypeVar, Union
from dataclasses import dataclass

T = TypeVar("T")

@dataclass
class HighlightedPart:
    characters: str

@dataclass
class PlainPart:
    characters: str

OptionPart = Union[PlainPart, HighlightedPart]

@dataclass
class Option(Generic[T]):
    parts: List[OptionPart]
    payload: T

    def get_text(self):
        text = ""
        for part in self.parts:
            text += part.characters
        return text
