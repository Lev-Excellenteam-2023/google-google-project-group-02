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


def find_match(user_input: List[str], data: FileData) -> List[Tuple]:
    """
    This function the best 5 sentence that match to the given string.
    :param user_input: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """

    suggestions: list = list()
    first_word = user_input[0]

    for index_word in data.words_graph.graph[first_word]:
        row_content = data.get_line(index_word.file, index_word.row)
        str_input = ' '.join(user_input)
        if str_input in row_content:
            suggestions += [(row_content, index_word.file, index_word.row)]
    return list(set(suggestions))


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
        return sentence.find(user_input) != -1
    pre_str = user_input[:index]
    suf_str = user_input[index:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return sentence.find(pre_str) == 0 and sentence.find(suf_str) == index + 1


def sub_char(user_input: str, index: int, sentence: str, first_word_index: int) -> bool:
    if index == 0:
        suf_str = user_input[index + 1:]
        return sentence.find(suf_str) != -1
    pre_str = user_input[:index]
    suf_str = user_input[index + 1:]
    sentence = cut_sentence_till_first_word(sentence, first_word_index)
    return sentence.find(pre_str) == 0 and sentence.find(suf_str) == index


def find_replace_one_char(user_input: str, sentence: str, first_word_index: int):
    for index in range(len(user_input)):
        if replaced_char(user_input, index, sentence, first_word_index):
            pass


def find_suggestions_with_a_mistake(user_input: str, data: FileData, first_word: str, num_of_found_suggestions: int) \
        -> List[Tuple]:
    suggests = list()
    if len(first_word) < 5:
        for index_word in data.words_graph.graph[first_word]:
            file_index = index_word.file
            row_index = index_word.row
            word_offset = index_word.offset
            for iterator in range(5, len(user_input)):
                if replaced_char(user_input, iterator, data.get_line(file_index, row_index), word_offset):
                    suggests.append((file_index, row_index))

    # for
    # suggests = list()
    # if len(first_word) < 5:
    #     for index_word in data.words_graph.graph[first_word]:
    #         file_index = index_word.file
    #         row_index = index_word.row
    #         word_offset = index_word.offset
    #         for iterator in range(5, len(user_input)):
    #             if replaced_char(user_input, iterator, data.get_line(file_index, row_index), word_offset):
    #                 suggests.append((file_index, row_index))
    # suggests = add_row_content(suggests, data)
    # if len(suggests) > 5:
    #     return suggests

    # return suggests


def match_first_word_mistaken(user_input: List[str], data: FileData) -> List[Tuple]:
    """
    This function find the sentences that match the user input when there are a mistake in the first word.
    :param user_input: the user input
    :param data: the data of the files
    :return: the sentences that match the user input when there are a mistake in the first word
    """

    if not user_input:
        return []

    suggestions: List[Tuple] = []
    alternatives: Set[str] = find_alternative_words(user_input[0])

    for alternative in alternatives:
        suggestions += find_match([alternative] + user_input[1:], data)

    return suggestions


def sort_and_filter_first_k(suggestions: List[Tuple], k: int) -> List[Tuple]:
    """
    This function sort the given list and return the first k elements.
    :param suggestions: all the suggestions
    :param k: the number of elements to return
    :return: the first k elements
    """

    suggestions.sort(key=lambda x: x[0].lower())
    return suggestions[:k]


def find_top_five_completions(user_input: List[str], data: FileData) -> List[Tuple]:

    first_word = user_input[0]
    suggestions = list()
    if first_word in data.words_graph.graph:
        suggestions = find_match(user_input, data)
        return sort_and_filter_first_k(suggestions, 5)

    #     if len(suggestions) < 5:
    #         new_suggestions = find_suggestions_with_a_mistake(' '.join(user_input), data, first_word, len(suggestions))
    #         if len(suggestions) + len(new_suggestions) > 5:
    #             new_suggestions = sort_and_filter_first_k(new_suggestions, 5 - len(suggestions))
    #         suggestions += new_suggestions
    #     if len(suggestions) < 5:
    #         new_suggestions = match_first_word_mistaken(user_input, data, len(suggestions))
    #         if len(suggestions) + len(new_suggestions) > 5:
    #             new_suggestions = sort_and_filter_first_k(new_suggestions, 5 - len(suggestions))
    #         suggestions += new_suggestions
    # else:
    #     suggestions = match_first_word_mistaken(user_input, data)
    # return suggestions


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
