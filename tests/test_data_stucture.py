from src.data_structure.data_structure import WordData, WordsGraph


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

