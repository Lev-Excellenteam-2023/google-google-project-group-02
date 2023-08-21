from __future__ import annotations
from dataclasses import dataclass
from typing import List
from data_class.file_data import FileData


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

    def find_match(self, my_str: List[str], data: FileData) -> List[(int, int)]:
        """
        This function the best 5 sentence that match to the given string.
        :param my_str: the given string
        :param data: the data of the files
        :return: the best 5 sentence that match to the given string
        """

        suggestions: List[(int, int)] = []

        for word in my_str:
            if word in self.graph:
                for index_word in self.graph[word]:
                    if ''.join(my_str) in data.get_line(index_word[0], index_word[1]):
                        suggestions += [(index_word[0], index_word[1])]

        return suggestions
