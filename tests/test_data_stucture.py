from data_structure.data_structure import WordData, WordsGraph
from data_class.file_data import FileData


def test_is_my_neighbors() -> None:
    my_word_data: WordData = WordData(0, 0, 0)
    my_second_word_data: WordData = WordData(0, 0, 1)

    assert my_word_data.is_my_neighbors(my_second_word_data) is True
    assert my_second_word_data.is_my_neighbors(my_word_data) is False


def test_add_word() -> None:
    my_struct: WordsGraph = WordsGraph()
    my_word_data: WordData = WordData(0, 0, 0)
    my_second_word_data: WordData = WordData(0, 0, 1)

    my_struct.add_word("hello", my_word_data)

    assert my_struct.graph["hello"] == [my_word_data]
    assert my_struct.graph["hello"] != [my_second_word_data]


def test_find_match() -> None:
    # Todo
    """
    my_struct: WordsGraph = WordsGraph()

    files: FileData = FileData()
    files.add_file('google', '1\n\nch01.qxd\n\n1/3/2001\n\n2\n\n9:44 AM\n\nChapter 1\n\nPage 2\n\n•\n\nIntroduction '
                             'to Networking and the OSI Model\n\nsend back to the mainframe. For this reason, '
                             'these terminals were often')

    assert my_struct.find_match(["send"], files) == [(0, 9)]
    """
