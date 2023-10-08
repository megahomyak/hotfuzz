from typing import Dict, List, Union

from hotfuzz.item import ItemIndex


Char = str


class FreeNode:
    def __init__(self, tree: Dict[Char, "Node"]):
        self.tree = tree

class OccupiedNode:
    def __init__(self, item_index: ItemIndex):
        self.item_index = item_index

Node = Union[OccupiedNode, FreeNode]


class HotCollision(Exception):
    pass


HotOutput = Union[List[ItemIndex], ItemIndex, None]


class Hot:

    def __init__(self, items: List[str]):
        self.tree: Dict[Char, Node] = {}
        for item_index, item in enumerate(items):
            tree = self.tree
            characters = filter(
                lambda character: character.isupper(),
                iter(item)
            )
            try:
                previous_character = next(characters)
            except StopIteration:
                pass
            else:
                for current_character in characters:
                    try:
                        node = tree[previous_character]
                    except KeyError:
                        new_tree = {}
                        tree[previous_character] = FreeNode(new_tree)
                        tree = new_tree
                    else:
                        if isinstance(node, FreeNode):
                            tree = node.tree
                        elif isinstance(node, OccupiedNode):
                            raise HotCollision()
                    previous_character = current_character
                tree[previous_character] = OccupiedNode(item_index)

    def search(self, query: str) -> HotOutput:
        tree = self.tree
        for character in query:
            try:
                node = tree[character]
            except KeyError:
                return None
            if isinstance(node, OccupiedNode):
                return node.item_index
            elif isinstance(node, FreeNode):
                tree = node.tree
        results = []
        trees_to_visit = [tree]
        while trees_to_visit:
            tree = trees_to_visit.pop()
            for node in tree.values():
                if isinstance(node, OccupiedNode):
                    results.append(node.item_index)
                elif isinstance(node, FreeNode):
                    trees_to_visit.append(node.tree)
        return results
