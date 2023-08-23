from data_structure.file_data import FileData
from suggest_engine.suggest import find_match, replaced_char, add_char, sub_char, \
    sort_and_filter_first_k, get_score, find_mistaken_suggestions

data = FileData('..\\private\\my_files')


def test_find_match():
    result_list_1 = find_match('in thi', data, 'in')
    assert result_list_1 == [(0, 2)]
    result_list_2 = find_match(['in', 'tji'], data)
    assert result_list_2 == []


def test_replace_char():
    assert replaced_char('my bode', 3, 'this is my code it is very nice', 2)
    assert not replaced_char('my bode', 4, 'this is my code it is very nice', 2)
    assert replaced_char('vmy code', 0, 'this is my code it is very nice', 2)
    assert replaced_char('my codo', 6, 'this is my code it is very nice', 2)


def test_add_char():
    assert add_char('my cde', 4, 'this is my code it is very nice', 2) == 'my code'
    assert not add_char('my cde', 3, 'this is my code it is very nice', 2) == 'my code'
    assert add_char('my coe', 5, 'this is my code it is very nice', 2) == 'my code'
    assert add_char('y code', 0, 'this is my code it is very nice', 2) == 'my code'


def test_sub_char():
    assert sub_char('my cdode', 4, 'this is my code it is very nice', 2) == 'my code'
    assert not sub_char('my cdode', 2, 'this is my code it is very nice', 2) == 'my code'
    assert not sub_char('my coded', 8, 'this is my code it is very nice', 2) == 'my code'
    assert sub_char('dmy code', 0, 'this is my code it is very nice', 2) == 'my code'


def test_sort_and_filter_first_k():
    try_list = [('hi', 1, 5), ('go', 2, 17), ('python', 3, 5), ('went', 7, 5), ('apple', 10, 5), ('git', 15, 5)]
    res_list = [('apple', 10, 5), ('git', 15, 5), ('go', 2, 17), ('hi', 1, 5), ('python', 3, 5)]
    assert sort_and_filter_first_k(try_list, 5) == res_list


def test_get_score():
    #
    assert get_score('my code', 'my code') == 14
    assert get_score('my core', 'my code') == 11
    assert get_score('my lode', 'my code') == 10
    assert get_score('mylcore', 'my code') == 9
    assert get_score('mi core', 'my code') == 8
    assert get_score('ny core', 'my code') == 7
    #
    assert get_score('my codre', 'my code') == 12
    assert get_score('my pcode', 'my code') == 10
    assert get_score('myp code', 'my code') == 8
    assert get_score('mpy code', 'my code') == 6
    assert get_score('lmy code', 'my code') == 4
    #
    assert get_score('my coe', 'my code') == 10
    assert get_score('my ode', 'my code') == 8
    assert get_score('mycode', 'my code') == 6
    assert get_score('m code', 'my code') == 4
    assert get_score('y code', 'my code') == 2


def test_get_mistakes():
    suggests = find_mistaken_suggestions('is nmot', data, 'is', 0)
    assert suggests == [('It is not possible to use these functions on objects that are not', 0, 8)]
    assert find_mistaken_suggestions('is nt', data, 'is', 0) == [
        ('It is not possible to use these functions on objects that are not', 0, 8)]
