from typing import List
from data_class.file_data import FileData


def find_match(my_str: List[str], data: FileData) -> List[(int, int)]:
    """
    This function the best 5 sentence that match to the given string.
    :param my_str: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """

    suggestions: List[(int, int)] = []

    if my_str and my_str[0] in data.words_graph.graph:
        for index_word in data.words_graph.graph[my_str[0]]:
            if ''.join(my_str) in data.get_line(index_word[0], index_word[1]):
                suggestions += [(index_word[0], index_word[1])]

    return suggestions
