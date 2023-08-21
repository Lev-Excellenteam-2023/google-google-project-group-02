from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class WordData:
    """
    This class save the data of a word.
    """

    file: int
    row: int
    offset: int

    def is_my_neighbors(self, word: WordData) -> bool:
        """
        This function check if two words are in the same file,
        row and the second word is the next word of the first word.
        :param word: second word
        :return: True if the second word is the neighbor of the first word, else False
        """

        if self.file == word.file and self.row == word.row and self.offset + 1 == word.offset:
            return True
        return False


class WordsGraph:
    """
    This class save all the words into a data structure.
    """

    graph: dict[str, [WordData]]

    def __init__(self) -> None:
        self.graph = dict()

    def add_word(self, word: str, word_data: WordData) -> None:
        """
        This function add a word to the data structure.
        :param word: the word
        :param word_data: it's data
        :return: None
        """

        if word in self.graph:
            self.graph[word] += [word_data]
        else:
            self.graph[word] = [word_data]

    def find_match(self, my_str: List[str]) -> List[(int, int)]:
        # TODO
        return []





