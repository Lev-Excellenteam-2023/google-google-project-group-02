import os
from typing import List
from util.consts import FILE_CONTENT

from util.remove_punctuation_util import process_sentence
from data_structure.data_structure import WordData, WordsGraph


class FileData:
    """
    A class that will save the data lines in a dict - each file will get an index as a key and the value will be a
    tuple with 2 organs. the first organ will be the file name and the second will be a list with the lines data -
    each organ is a string of the specific line
    """

    data_dict: dict
    words_graph: WordsGraph
    free_index: int

    def __init__(self, path):
        self.data_dict = dict()
        self.free_index = 0
        self.words_graph = WordsGraph()
        self.add_all_files_from_path(path)
        self.load_words_graph()

    def add_all_files_from_path(self, path: str) -> None:
        """
        Gets the path that contains the file and adds to data_dict the name and content of the file.
        :param path: The main path
        """
        for filename in os.listdir(path):
            file_path: str = os.path.join(path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding="utf8") as file:
                    content: str = file.read()
                    self.add_file(filename, content)
            elif os.path.isdir(file_path):
                self.add_all_files_from_path(file_path)

    def add_file(self, file_name: str, file_data: str) -> None:
        """
        The func adds a new file to the dictionary

        :param file_name: The file name
        :param file_data: The data that is contained in the file
        :return: None
        """
        data_split_by_lines: List[str] = file_data.split('\n')
        self.data_dict[self.free_index] = (file_name, data_split_by_lines)
        self.free_index += 1

    def load_words_graph(self) -> None:
        """
        Goes over the data in data_dict and adds the words to words_graph
        """
        for key in self.data_dict:
            for row_index, row in enumerate(self.data_dict[key][FILE_CONTENT]):
                clean_words: List[str] = process_sentence(self.data_dict[key][FILE_CONTENT][row_index])
                for index, word in enumerate(clean_words):
                    word_data: WordData = WordData(key, row_index, index)
                    self.words_graph.add_word(word, word_data)

    def get_line(self, file_index: int, line_index: int) -> str:
        """
        Gets the content of a line in a file
        :param file_index: The file who owns the line
        :param line_index: The index of line
        :return: The content
        """
        try:
            return self.data_dict[file_index][FILE_CONTENT][line_index]
        except KeyError:
            return 'There no such file_index or line_index'
