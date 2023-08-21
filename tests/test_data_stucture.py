from data_structure.data_structure import WordData, WordsGraph


def test_is_my_neighbors() -> None:
    my_word_data: WordData = WordData(0, 0, 0)
    my_second_word_data: WordData = WordData(0, 0, 1)

    assert my_word_data.is_my_neighbors(my_second_word_data) is True
    assert my_second_word_data.is_my_neighbors(my_word_data) is False


def test_add_word():
    my_struct: WordsGraph = WordsGraph()
    my_word_data: WordData = WordData(0, 0, 0)
    my_second_word_data: WordData = WordData(0, 0, 1)

    my_struct.add_word("hello", my_word_data)

    assert my_struct.graph["hello"] == [my_word_data]
    assert my_struct.graph["hello"] != [my_second_word_data]


def test_find_match():
    my_struct: WordsGraph = WordsGraph()

    my_struct.add_word("hello", WordData(0, 0, 0))
    my_struct.add_word("world", WordData(0, 0, 1))
    my_struct.add_word("this", WordData(0, 0, 2))
    my_struct.add_word("is", WordData(0, 0, 3))
    my_struct.add_word("a", WordData(0, 0, 4))
    my_struct.add_word("test", WordData(0, 0, 5))

    my_struct.add_word("hello", WordData(1, 0, 0))
    my_struct.add_word("python", WordData(1, 0, 1))

    assert my_struct.find_match(["hello"]) == [(0, 0), (1, 0)]
