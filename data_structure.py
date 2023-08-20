from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class WordData:
    file: int
    row: int
    offset: int
    next_word: str or None

    def is_my_neighbors(self, word: WordData) -> bool:
        if self.file == word.file and self.row == word.row and self.offset == word.offset + 1:
            return True
        return False


class WordsGraph:
    graph: dict[str, [WordData]]

    def __init__(self):
        self.graph = dict()

    def add_word(self, word: str, word_data: WordData):
        if word in self.graph:
            self.graph[word] += [word_data]
        else:
            self.graph[word] = [word_data]


