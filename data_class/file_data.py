import os
import re
from typing import List
from Utils.consts import FILE_NAME, FILE_CONTENT


class FileData:
    """
    A class that will save the data lines in a dict - each file will get an index as a key and the value will be a
    tuple with 2 organs. the first organ will be the file name and the second will be a list with the lines data -
    each organ is a string of the specific line
    """

    data_dict: dict
    words_graph: dict
    free_index: int

    def __init__(self, path):
        self.data_dict = dict()
        self.free_index = 0
        self.add_all_files_from_path(path)
        # self.load_words_graph()

    def add_all_files_from_path(self, path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding="utf8") as file:
                    content = file.read()
                    self.add_file(filename, content)
            elif os.path.isdir(file_path):
                self.add_all_files_from_path(file_path)

    def add_file(self, file_name: str, file_data: str):
        """
        The func adds a new file to the dictionary

        :param file_name: The file name
        :param file_data: The data that is contained in the file
        :return: None
        """
        data_splitted_by_lines: List[str] = re.split('\n+', file_data)
        self.data_dict[self.free_index] = (file_name, data_splitted_by_lines)
        self.free_index += 1

    # def load_words_graph(self):
    #     for key in self.data_dict:
    #         for line in self.data_dict[key][FILE_CONTENT]:
    #     pass

    def get_line(self, file_index: int, line_index: int) -> str:
        """
        Gets the content of a line in a file
        :param file_index: The file who owns the line
        :param line_index: The index of line
        :return: The content
        """
        try:
            return self.data_dict[file_index][FILE_CONTENT][line_index]
        except:
            return 'There no such file_index or line_index'
