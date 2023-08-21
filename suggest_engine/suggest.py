from typing import List
from data_structure.data_structure import WordsGraph
from data_class.file_data import FileData


def find_match(graph: WordsGraph, my_str: List[str], data: FileData) -> List[(int, int)]:
    """
    This function the best 5 sentence that match to the given string.
    :param graph: the data structure
    :param my_str: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """

    suggestions: List[(int, int)] = []

    for word in my_str:
        if word in graph:
            for index_word in graph[word]:
                if ''.join(my_str) in data.get_line(index_word[0], index_word[1]):
                    suggestions += [(index_word[0], index_word[1])]

    return suggestions
