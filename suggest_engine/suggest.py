from typing import List, Tuple, Set
from data_class.file_data import FileData
import string


def help_get_score(user_input: str, sentence_substring: str, score: int, score_to_sub: int) -> int:
    if user_input[:5] == sentence_substring[:5]:
        return score - score_to_sub
    for iterator in range(5):
        if user_input[iterator] != sentence_substring[iterator]:
            score -= (5 - iterator) * score_to_sub
            break
    return score


def get_score(user_input: str, sentence_substring: str) -> int:
    score = len(user_input) * 2
    if user_input == sentence_substring:
        return score
    if len(user_input) == len(sentence_substring):
        score -= 2
        return help_get_score(user_input, sentence_substring, score, 1)
    elif len(user_input) > len(sentence_substring):
        score -= 2
        return help_get_score(user_input, sentence_substring, score, 2)
    else:
        return help_get_score(user_input, sentence_substring, score, 2)


def find_match(user_input: str, data: FileData, first_word: str) -> list:
    """
    This function the best 5 sentence that match to the given string.
    :param user_input: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """

    suggestions: list = list()
    if first_word in data.words_graph.graph:
        for index_word in data.words_graph.graph[first_word]:
            row_content = data.get_line(index_word.file, index_word.row)
            if user_input in row_content:
                suggestions += [(row_content, index_word.file, index_word.row)]

    return list(set(suggestions))


def cut_sentence_till_first_word(sentence: str, index: int) -> str:
    split_sentence = sentence.split()
    cut_sentence = ' '.join(split_sentence[iter] for iter in range(index, len(split_sentence)))
    return cut_sentence


def replaced_char(user_input: str, index: int, sentence: str, first_word_index: int) -> str:
    if user_input in sentence:
        return ''
    user_input_len = len(user_input)
    if index == user_input_len - 1:
        sentence = cut_sentence_till_first_word(sentence, first_word_index)
        if len(sentence) < user_input_len:
            return ''
        pre_str = user_input[:index]
        return '' if sentence.find(pre_str) == -1 else sentence[:index + 1]
    if index == 0:
        suf_str = user_input[1:]
        find_index = sentence.find(suf_str)
        return '' if find_index <= 0 else sentence[find_index: find_index + len(user_input)]
    pre_str = user_input[:index]
    suf_str = user_input[index + 1:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return '' if sentence.find(pre_str) != 0 or sentence.find(suf_str) != index + 1 else sentence[:user_input_len]


def add_char(user_input: str, index: int, sentence: str, first_word_index: int) -> str:
    if user_input in sentence:
        return ''
    end_index: int = len(user_input) + 1
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    if index == 0:
        return '' if sentence.find(user_input) == -1 else sentence[: end_index]
    pre_str = user_input[:index]
    suf_str = user_input[index:]
    return '' if sentence.find(pre_str) != 0 or sentence.find(suf_str) != index + 1 else sentence[: end_index]


def sub_char(user_input: str, index: int, sentence: str, first_word_index: int) -> str:
    if user_input in sentence:
        return ''
    end_index: int = len(user_input) - 1
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    if index == 0:
        suf_str = user_input[index + 1:]
        return '' if sentence.find(suf_str) == -1 else sentence[:end_index]
    pre_str = user_input[:index]
    suf_str = user_input[index + 1:]
    return '' if sentence.find(pre_str) != 0 or sentence.find(suf_str) != index else sentence[:end_index]


def find_suggestions_with_a_mistake(user_input: str, data: FileData, first_word: str, num_of_found_suggestions: int) \
        -> list:
    suggests = list()
    first_word_len = len(first_word)
    user_input_len = len(user_input)
    for index_word in data.words_graph.graph[first_word]:
        row_content = data.get_line(index_word.file, index_word.row)
        for index in range(first_word_len + 1, user_input_len):
            substring_sentence = add_char(user_input, index, row_content, index_word.offset)
            if substring_sentence != '':
                score = get_score(user_input, substring_sentence)
                suggests += [(row_content, index_word.file, index_word.row, score)]
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < 5:
        for index_word in data.words_graph.graph[first_word]:
            row_content = data.get_line(index_word.file, index_word.row)
            for index in range(first_word_len + 1, user_input_len):
                substring_sentence = replaced_char(user_input, index, row_content, index_word.offset)
                if substring_sentence != '':
                    score = get_score(user_input, substring_sentence)
                    suggests += [(row_content, index_word.file, index_word.row, score)]
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < 5:
        for index_word in data.words_graph.graph[first_word]:
            row_content = data.get_line(index_word.file, index_word.row)
            for index in range(first_word_len + 1, user_input_len):
                substring_sentence = sub_char(user_input, index, row_content, index_word.offset)
                if substring_sentence != '':
                    score = get_score(user_input, substring_sentence)
                    suggests += [(row_content, index_word.file, index_word.row, score)]
    return list(set(suggests))


def match_first_word_mistaken(user_input: List[str], data: FileData) -> list:
    if not user_input:
        return []

    user_str = ' '.join(user_input)
    suggestions: list = []
    alternatives: Set[str] = find_alternative_words(user_input[0])

    for alternative in alternatives:
        alternative_input = ' '.join([alternative] + user_input[1:])
        new_suggestions = find_match(alternative_input, data, alternative)
        new_suggestions = [list(suggestion) for suggestion in new_suggestions]
        [suggestion.append(get_score(user_str, alternative_input)) for suggestion in new_suggestions]
        new_suggestions = [tuple(suggestion) for suggestion in new_suggestions]
        suggestions += new_suggestions

    return list(set(suggestions))


def sort_and_filter_first_k(suggestions: list, k: int) -> list:
   """
    This function sort the given list and return the first k elements.
    :param suggestions: all the suggestions
    :param k: the number of elements to return
    :return: the first k elements
    """
    suggestions.sort(key=lambda x: (-x[3], x[0].lower()))
    return suggestions[:k]


def find_top_five_completions(user_input: List[str], data: FileData) -> List[Tuple]:

    first_word = user_input[0]
    suggestions = list()
    str_input = ' '.join(user_input)
    if first_word in data.words_graph.graph:
        suggestions += find_match(str_input, data, first_word)
        suggestions = [list(suggestion) for suggestion in suggestions]
        [suggestion.append(len(str_input) * 2) for suggestion in suggestions]
        if len(suggestions) < 5:
            new_suggestions = find_suggestions_with_a_mistake(str_input, data, first_word, len(suggestions))
            new_suggestions = [list(suggestion) for suggestion in new_suggestions]
            suggestions += new_suggestions
        if len(suggestions) < 5:
            new_suggestions = match_first_word_mistaken(user_input, data)
            new_suggestions = [list(suggestion) for suggestion in new_suggestions]
            suggestions += new_suggestions
    else:
        suggestions += match_first_word_mistaken(user_input, data)
        suggestions = [list(suggestion) for suggestion in suggestions]
    sorted_suggestions = sort_and_filter_first_k(suggestions, 5)
    [suggestion.pop(3) for suggestion in sorted_suggestions]
    tuple_suggestions = [tuple(suggestion) for suggestion in sorted_suggestions]
    return tuple_suggestions


def find_alternative_words(word: str) -> Set[str]:
    """
    Find all the words that can be created by adding, removing or replacing one character in the given word.
    :param word: The word to find alternatives for.
    :return: All the words with one character difference from the given word.
    """

    alphabet: List[str] = list(string.ascii_lowercase)
    alternatives: Set[str] = set()

    for index, _ in enumerate(word):
        for letter in alphabet:
            alternatives.add(word[:index] + letter + word[index:])
            alternatives.add(word[:index + 1] + letter + word[index + 1:])
            alternatives.add(word[:index] + letter + word[index + 1:])
            alternatives.add(word[:index] + word[index + 1:])

    return alternatives - {word, ''}
