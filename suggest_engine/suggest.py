from typing import List, Tuple, Set
from data_class.file_data import FileData
import string


def help_get_score(user_input: str, sentence_substring: str, score: int, score_to_sub: int) -> int:
    """

    Calculate a modified score based on user input and a sentence substring.

    This function takes a user's input, a sentence substring, an initial score, and a score reduction value.
    It compares characters of the user input and sentence substring and calculates the modified score.

    :param user_input: A string containing the user's input.
    :param sentence_substring: A string containing a substring of a sentence to compare with.
    :param score: An integer representing the initial score.
    :param score_to_sub: An integer representing the score reduction value.
    :return: An integer representing the modified score.
    """
    if user_input[:5] == sentence_substring[:5]:
        return score - score_to_sub
    for iterator in range(min(5, len(user_input), len(sentence_substring))):
        if user_input[iterator] != sentence_substring[iterator]:
            score -= (5 - iterator) * score_to_sub
            break
    return score


def get_score(user_input: str, sentence_substring: str) -> int:
    """
    Calculate a score based on user input and a sentence substring.

    This function takes a user's input and a sentence substring, assigns an initial score based on the length of the user input,
    and then calculates a modified score using the 'help_get_score' function based on the comparison between the two strings.

    :param user_input: A string containing the user's input.
    :param sentence_substring: A string containing a substring of a sentence to compare with.
    :return: An integer representing the calculated score.
    """
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
    :param first_word: The first word of the user
    :param user_input: the given string
    :param data: the data of the files
    :return: the best 5 sentence that match to the given string
    """

    suggestions: list = list()
    if first_word in data.words_graph.graph:
        for index_word in data.words_graph.graph[first_word]:
            row_content = data.get_line(index_word.file, index_word.row)
            if user_input in row_content and (row_content, index_word.file, index_word.row):
                suggestions += [[row_content, index_word.file, index_word.row]]

    return remove_duplicates(suggestions)


def cut_sentence_till_first_word(sentence: str, index: int) -> str:
    """
    Cut a sentence from the specified index to the end, preserving the first word.

    This function takes a sentence and an index and returns a modified sentence where only the words
    from the specified index to the end are included, with the first word preserved.

    :param sentence: A string containing the input sentence.
    :param index: An integer representing the starting index for cutting the sentence.
    :return: A string containing the modified sentence.
    """
    split_sentence = sentence.split()
    cut_sentence = ' '.join(split_sentence[iter] for iter in range(index, len(split_sentence)))
    return cut_sentence


def replaced_char(user_input: str, index: int, sentence: str, first_word_index: int) -> str:
    """
    Replace a character at a specified index in the user input with a character from the sentence.

    :param user_input: A string containing the user's input.
    :param index: An integer representing the index of the character to replace in the user input.
    :param sentence: A string containing the sentence to extract the replacement character from.
    :param first_word_index: An integer representing the index of the first word in the sentence.
    :return: A string with the character replaced, or an empty string if no replacement can be made.
    """
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
    """
    Add a character at a specified index in the user input by extracting it from the sentence.

    :param user_input: A string containing the user's input.
    :param index: An integer representing the index in the user input where the character should be added.
    :param sentence: A string containing the sentence to extract the character from.
    :param first_word_index: An integer representing the index of the first word in the sentence.
    :return: A string with the character added, or an empty string if no addition can be made.
    """
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
    """
    Substitute a character at a specified index in the user input with a character from the sentence.

    :param user_input: A string containing the user's input.
    :param index: An integer representing the index of the character to substitute in the user input.
    :param sentence: A string containing the sentence to extract the replacement character from.
    :param first_word_index: An integer representing the index of the first word in the sentence.
    :return: A string with the character substituted, or an empty string if no substitution can be made.
    """
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


def find_mistaken_suggestions_helper(user_input: str, data: FileData, first_word: str, first_word_len: int,
                                     user_input_len: int, func) -> list:
    """
    Helper function to find suggestions for one mistaken input based on a given function.

    :param user_input: A string containing the user's input.
    :param data: A FileData object containing data for suggestions.
    :param first_word: A string representing the first word in the user input.
    :param first_word_len: An integer representing the length of the first word.
    :param user_input_len: An integer representing the length of the user input.
    :param func: A function used for generating suggestions (e.g., add_char, replaced_char, sub_char).
    :return: A list of suggestions as tuples.
    """
    suggests = list()
    for index_word in data.words_graph.graph[first_word]:
        row_content = data.get_line(index_word.file, index_word.row)
        for index in range(first_word_len + 1, user_input_len):
            substring_sentence = func(user_input, index, row_content, index_word.offset)
            if substring_sentence != '':
                score = get_score(user_input, substring_sentence)
                suggests += [(row_content, index_word.file, index_word.row, score)]
    return suggests


def find_mistaken_suggestions(user_input: str, data: FileData, first_word: str, num_of_found_suggestions: int) \
        -> list:
    """
    Find mistaken input suggestions based on the user's input and data.

    :param user_input: A string containing the user's input.
    :param data: A FileData object containing data for suggestions.
    :param first_word: A string representing the first word in the user input.
    :param num_of_found_suggestions: An integer representing the number of found suggestions.
    :return: A list of suggestions as tuples.
    """
    suggests = list()
    first_word_len = len(first_word)
    user_input_len = len(user_input)
    suggests += find_mistaken_suggestions_helper(user_input, data, first_word, first_word_len, user_input_len, add_char)
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < 5:
        suggests += find_mistaken_suggestions_helper(user_input, data, first_word, first_word_len, user_input_len,
                                                     replaced_char)
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < 5:
        suggests += find_mistaken_suggestions_helper(user_input, data, first_word, first_word_len, user_input_len,
                                                     sub_char)
    return remove_duplicates(suggests)


def remove_duplicates(suggestions: list) -> list:
    """
    Remove duplicate suggestions from a list of suggestions.

    :param suggestions: A list of suggestions as tuples.
    :return: A list of suggestions with duplicates removed.
    """
    tuple_suggestions = [tuple(suggestion) for suggestion in suggestions]
    set_suggestions = list(set(tuple_suggestions))
    return [list(suggestion) for suggestion in suggestions]


def match_first_word_mistaken(user_input: List[str], data: FileData) -> list:
    """
    Find suggestions for mistaken input by considering alternative first words.

    :param user_input: A list of strings representing the user's input.
    :param data: A FileData object containing data for suggestions.
    :return: A list of suggestions as tuples.
    """
    if not user_input:
        return []

    user_str = ' '.join(user_input)
    suggestions: list = []
    alternatives: Set[str] = find_alternative_words(user_input[0])

    for alternative in alternatives:
        alternative_input = ' '.join([alternative] + user_input[1:])
        new_suggestions = find_match(alternative_input, data, alternative.split(' ')[0])
        if new_suggestions:
            [suggestion.append(get_score(user_str, alternative_input)) for suggestion in new_suggestions]
        suggestions += new_suggestions

    return remove_duplicates(suggestions)


def sort_and_filter_first_k(suggestions: list, k: int) -> list:
    """
    Sort a list of suggestions by score from high to low and filter it, keeping the top k suggestions.

    :param suggestions: A list of suggestions as tuples.
    :param k: An integer representing the number of top suggestions to keep.
    :return: A list of the top k suggestions as tuples.
    """
    suggestions.sort(key=lambda x: (-x[3], x[0].lower()))
    return suggestions[:k]


def find_top_five_completions(user_input: List[str], data: FileData) -> List[Tuple]:
    """
    Find the top five completions for the user's input based on data.

    :param user_input: A list of strings representing the user's input.
    :param data: A FileData object containing data for suggestions.
    :return: A list of tuples representing the top five completions.
    """

    first_word = user_input[0]
    suggestions = list()
    str_input = ' '.join(user_input)
    if first_word in data.words_graph.graph:
        suggestions += find_match(str_input, data, first_word)
        [suggestion.append(len(str_input) * 2) for suggestion in suggestions]
        if len(suggestions) < 5:
            new_suggestions = find_mistaken_suggestions(str_input, data, first_word, len(suggestions))
            suggestions += new_suggestions
        if len(suggestions) < 5:
            new_suggestions = match_first_word_mistaken(user_input, data)
            suggestions += new_suggestions
    else:
        suggestions += match_first_word_mistaken(user_input, data)
    sorted_suggestions = sort_and_filter_first_k(suggestions, 5)
    [suggestion.pop(3) for suggestion in sorted_suggestions]
    return sorted_suggestions


def find_alternative_words(word: str) -> Set[str]:
    """
    Generate alternative words by inserting, removing or replacing a space or a letter within a word.

    :param word: A string representing the word for which alternative words are generated.
    :return: A set of alternative words.
    """

    alphabet: List[str] = list(string.ascii_lowercase)
    alphabet.append(' ')
    alternatives: Set[str] = set()

    for index in range(len(word) + 1):
        for letter in alphabet:
            alternatives.add(word[:index] + letter + word[index:])
            alternatives.add(word[:index] + letter + word[index + 1:])
            alternatives.add(word[:index] + word[index + 1:])

    return alternatives - {word, ''}
