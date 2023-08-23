from src.data_structure.file_data import FileData
from src.suggest_engine.suggest import find_match, replaced_char, add_char, sub_char, \
    sort_and_filter_first_k, get_score, find_mistaken_suggestions

data = FileData('..\\Archive\\my_files')


def test_find_match():
    result_list_1 = find_match('with wide', data, 'with')
    assert result_list_1 == [['of their type, or with wide classes of object types (e.g. all', 0, 4]]
    result_list_2 = find_match('with wive', data, 'with')
    assert result_list_2 == []


def test_replace_char():
    assert replaced_char('my bode', 3, 'this is my code it is very nice', 2) == 'my code'
    assert replaced_char('my bode', 4, 'this is my code it is very nice', 2) == ''
    assert replaced_char('my codo', 6, 'this is my code it is very nice', 2) == 'my code'


def test_add_char():
    assert add_char('my cde', 4, 'this is my code it is very nice', 2) == 'my code'
    assert add_char('my cde', 3, 'this is my code it is very nice', 2) == ''
    assert add_char('my coe', 5, 'this is my code it is very nice', 2) == 'my code'


def test_sub_char():
    assert sub_char('my cdode', 4, 'this is my code it is very nice', 2) == 'my code'
    assert sub_char('my cdode', 2, 'this is my code it is very nice', 2) == ''
    assert sub_char('my coded', 7, 'this is my code it is very nice', 2) == ''


def test_sort_and_filter_first_k():
    try_list = [['hi', 1, 5, 15], ['go', 2, 17, 7], ['python', 3, 5, 44], ['went', 7, 5, 8], ['git', 15, 5, 44],
                ['apple', 10, 5, 40], ]
    res_list = [['git', 15, 5, 44], ['python', 3, 5, 44], ['apple', 10, 5, 40], ['hi', 1, 5, 15], ['went', 7, 5, 8]]
    assert sort_and_filter_first_k(try_list, 5) == res_list


def test_get_score():
    # match text
    assert get_score('my code', 'my code') == 14
    # replace
    assert get_score('my core', 'my code') == 11
    assert get_score('my lode', 'my code') == 10
    assert get_score('mylcore', 'my code') == 9
    assert get_score('mi core', 'my code') == 8
    assert get_score('ny core', 'my code') == 7
    # sub
    assert get_score('my codre', 'my code') == 12
    assert get_score('my pcode', 'my code') == 10
    assert get_score('myp code', 'my code') == 8
    assert get_score('mpy code', 'my code') == 6
    assert get_score('lmy code', 'my code') == 4
    # add
    assert get_score('my coe', 'my code') == 10
    assert get_score('my ode', 'my code') == 8
    assert get_score('mycode', 'my code') == 6
    assert get_score('m code', 'my code') == 4
    assert get_score('y code', 'my code') == 2


def test_get_mistakes():
    suggests = find_mistaken_suggestions('sequence tpes', data, 'sequence', 4)
    assert suggests == [['numerical types, or all sequence types).  When used on object types', 0, 5, 24]]
    assert find_mistaken_suggestions('sequence tyopes', data, 'sequence', 4) == [
        ['numerical types, or all sequence types).  When used on object types', 0, 5, 26]]
