from abc import ABC, abstractmethod
from typing import List, Union
from dataclasses import dataclass
from .option import Option, PlainPart, HighlightedPart


class Hot:
    def __init__(self, options: List[Option]):
        self.options_hotkeys = {}
        for option in options:
            base_dict = self.options_hotkeys
            chain = []
            highlighted = False
            for part in option.parts:
                if isinstance(part, HighlightedPart):
                    highlighted = True
                    for character in part.characters:
                        character = character.lower()
                        chain.append(character)
                        if "end" in base_dict:
                            raise HotkeyCollision(chain)
                        elif character not in base_dict:
                            base_dict[character] = {}
                        base_dict = base_dict[character]
            if highlighted:
                base_dict["end"] = option


@dataclass
class Selected:
    option: Option

@dataclass
class Options:
    options: List[Option]

Output = Union[Options, Selected]

class Filter(ABC):
    @abstractmethod
    def get_output(self, input: str) -> Output:
        pass

class HotFilter(Filter):
    def __init__(self, options: List[Option]) -> None:
        super().__init__()
        self.options = {}


    @abstractmethod
    def get_output(self, input: str) -> Output:
