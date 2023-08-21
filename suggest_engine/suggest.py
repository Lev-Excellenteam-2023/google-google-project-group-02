from typing import List
from data_structure.data_structure import WordsGraph
from data_class.file_data import FileData


def find_match(my_str: List[str], data: FileData) -> List[(int, int)]:
    """
    This function the best 5 sentence that match to the given string.
    :param my_str: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """
    suggestions: List[(int, int)] = []
    first_word = my_str[0]

    for index_word in data.words_graph.graph[first_word]:
        if ''.join(my_str) in data.get_line(index_word[0], index_word[1]):
            suggestions += [(index_word[0], index_word[1])]
    return suggestions


def cut_sentence_till_first_word(sentence: str, index: int) -> str:
    split_sentence = sentence.split()
    cut_sentence = ' '.join(split_sentence[iter] for iter in range(index, len(split_sentence)))
    return cut_sentence


def replaced_char(user_input: str, index: int, sentence: str, first_word_index: int) -> bool:
    if index == len(user_input) - 1:
        pre_str = user_input[:index]
        return sentence.find(pre_str) != -1
    if index == 0:
        suf_str = user_input[index + 1:]
        return sentence.find(suf_str) != -1
    pre_str = user_input[:index]
    suf_str = user_input[index + 1:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return sentence.find(pre_str) == 0 and sentence.find(suf_str) == index + 1


def add_char(user_input: str, index: int, sentence: str, first_word_index: int) -> bool:
    if index == 0:
        return sentence.find(user_input) == index + 1
    pre_str = user_input[:index]
    suf_str = user_input[index:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return sentence.find(pre_str) == 0 and sentence.find(suf_str) == index + 1


def sub_char(user_input: str, index: int, sentence: str, first_word_index: int) -> bool:
    if index == 0:
        suf_str = user_input[index + 1:]
        return sentence.find(suf_str) == index
    pre_str = user_input[:index]
    suf_str = user_input[index + 1:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return sentence.find(pre_str) == 0 and sentence.find(suf_str) == index


def find_suggestions_with_a_mistake(user_input: List[str], data: FileData, num_of_found_suggestions: int) \
        -> List[(int, int)]:
    pass


def match_first_word_mistaken(user_input: List[str], data: FileData, num_of_found_suggestions: int = 0) -> List[
    (int, int)]:
    pass


def find_top_five_completions(user_input: list, data: FileData):
    first_word = user_input[0]
    if first_word in data.words_graph.graph:
        suggestions = find_match(user_input, data)
        if len(suggestions) < 5:
            suggestions += find_suggestions_with_a_mistake(user_input, data, len(suggestions))
        if len(suggestions) < 5:
            suggestions += match_first_word_mistaken(user_input, data, len(suggestions))
    else:
        suggestions = match_first_word_mistaken(user_input, data)
    return suggestions
