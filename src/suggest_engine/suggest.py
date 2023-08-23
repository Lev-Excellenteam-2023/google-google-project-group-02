from typing import List, Tuple, Set, Callable
from src.data_structure.file_data import FileData
from src.util.remove_punctuation_util import process_sentence
from src.util.consts import MAX_SUGGESTION, INDEX_FOR_SCORE
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
    if user_input[:INDEX_FOR_SCORE] == sentence_substring[:INDEX_FOR_SCORE]:
        return score - score_to_sub
    for iterator in range(min(INDEX_FOR_SCORE, len(user_input), len(sentence_substring))):
        if user_input[iterator] != sentence_substring[iterator]:
            score -= (INDEX_FOR_SCORE - iterator) * score_to_sub
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
    score: int = len(user_input) * 2
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


def find_match(user_input: str, data: FileData, first_word: str) -> List[List]:
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
            row_content: str = data.get_line(index_word.file, index_word.row)
            clean_row_content: str = ' '.join(process_sentence(row_content))
            if user_input in clean_row_content:
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
    split_sentence: List[str] = sentence.split()
    cut_sentence: str = ' '.join(split_sentence[iter] for iter in range(index, len(split_sentence)))
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
    user_input_len: int = len(user_input)
    if index == user_input_len - 1:
        sentence: str = cut_sentence_till_first_word(sentence, first_word_index)
        if len(sentence) < user_input_len:
            return ''
        pre_str: str = user_input[:index]
        return '' if sentence.find(pre_str) == -1 else sentence[:index + 1]
    if index == 0:
        suf_str: str = user_input[1:]
        find_index: int = sentence.find(suf_str)
        return '' if find_index <= 0 else sentence[find_index: find_index + len(user_input)]
    pre_str: str = user_input[:index]
    suf_str: str = user_input[index + 1:]
    sentence: str = cut_sentence_till_first_word(sentence, first_word_index)
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
    sentence: str = cut_sentence_till_first_word(sentence, first_word_index)
    if index == 0:
        return '' if sentence.find(user_input) == -1 else sentence[: end_index]
    pre_str: str = user_input[:index]
    suf_str: str = user_input[index:]
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
    sentence: str = cut_sentence_till_first_word(sentence, first_word_index)
    if index == 0:
        suf_str: str = user_input[index + 1:]
        return '' if sentence.find(suf_str) == -1 else sentence[:end_index]
    pre_str: str = user_input[:index]
    suf_str: str = user_input[index + 1:]
    return '' if sentence.find(pre_str) != 0 or sentence.find(suf_str) != index else sentence[:end_index]


def find_mistaken_suggestions_helper(user_input: str, data: FileData, first_word: str, first_word_len: int,
                                     user_input_len: int, func: Callable) -> List[List]:
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
        row_content: str = data.get_line(index_word.file, index_word.row)
        clean_row_content: str = ' '.join(process_sentence(row_content))
        for index in range(first_word_len + 1, user_input_len):
            substring_sentence: str = func(user_input, index, clean_row_content, index_word.offset)
            if substring_sentence != '':
                score: int = get_score(user_input, substring_sentence)
                suggests += [(row_content, index_word.file, index_word.row, score)]
    return suggests


def find_certain_mistake(user_input: str, data: FileData, first_word: str, first_word_len: int, user_input_len: int,
                         func, error_type: str) -> List[List]:
    """
    Find and suggest corrections for a certain type mistakes in user input(add char, replace char and sub char).

    :param user_input: The user's input string for which mistakes are to be detected and suggestions provided.
    :param data: The dataset or FileData object containing information for mistake detection.
    :param first_word: The first word of the user's input.
    :param first_word_len: The length of the first word in characters.
    :param user_input_len: The total length of the user's input string.
    :param func: A function used for detecting mistakes in user input.
    :param error_type: The type of error to search for (e.g., spelling, grammar).

    :return: A list of suggested corrections or fixes for the detected mistakes.
    """
    suggests: List[List] = find_mistaken_suggestions_helper(user_input, data, first_word, first_word_len, user_input_len, func)
    if first_word_len >= MAX_SUGGESTION:
        suggests += match_first_word_mistaken(user_input.split(' '), data, error_type)
    return suggests


def find_mistaken_suggestions(user_input: str, data: FileData, first_word: str, num_of_found_suggestions: int) \
        -> List[List]:
    """
    Find mistaken input suggestions based on the user's input and data.

    :param user_input: A string containing the user's input.
    :param data: A FileData object containing data for suggestions.
    :param first_word: A string representing the first word in the user input.
    :param num_of_found_suggestions: An integer representing the number of found suggestions.
    :return: A list of suggestions as tuples.
    """
    first_word_len: int = len(first_word)
    user_input_len: int = len(user_input)

    suggests: List[List] = find_certain_mistake(user_input, data, first_word, first_word_len, user_input_len, add_char, 'add')
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < MAX_SUGGESTION:
        suggests += find_certain_mistake(user_input, data, first_word, first_word_len, user_input_len, replaced_char,
                                         'replace')
    num_of_found_suggestions += len(suggests)
    if num_of_found_suggestions < MAX_SUGGESTION:
        suggests += find_certain_mistake(user_input, data, first_word, first_word_len, user_input_len, sub_char, 'sub')
    return remove_duplicates(suggests)


def remove_duplicates(suggestions: List[List]) -> List[List]:
    """
    Remove duplicate suggestions from a list of suggestions.

    :param suggestions: A list of suggestions as tuples.
    :return: A list of suggestions with duplicates removed.
    """
    tuple_suggestions: List[Tuple] = [tuple(suggestion) for suggestion in suggestions]
    set_suggestions: List[Tuple] = list(set(tuple_suggestions))
    return [list(suggestion) for suggestion in set_suggestions]


def match_first_word_mistaken_helper(user_input: List[str], user_str: str, data, error_type: str) -> List[List]:
    """
    Generate suggestions based on alternative words for the first word in user input.

    :param user_input: A list of words in the user's input.
    :param user_str: The original user input string.
    :param data: The data or dataset used for generating suggestions.
    :param error_type: The type of error to consider (e.g., spelling, grammar).

    :return: A list of suggestions based on alternative first words.
    """
    alternatives: Set[str] = find_alternative_words(user_input[0], error_type)
    suggestions: List[List] = list()

    for alternative in alternatives:
        alternative_input: str = ' '.join([alternative] + user_input[1:])
        new_suggestions: List[List] = find_match(alternative_input, data, alternative.split(' ')[0])
        if new_suggestions:
            [suggestion.append(get_score(user_str, alternative_input)) for suggestion in new_suggestions]
        suggestions += new_suggestions
    return suggestions


def match_first_word_mistaken(user_input: List[str], data: FileData, error_type: str = 'all') -> List[List]:
    """
    Find suggestions for mistaken input by considering alternative first words.

    :param error_type: witch error to check
    :param num_of_found_suggestions: In order to know to stop by five
    :param user_input: A list of strings representing the user's input.
    :param data: A FileData object containing data for suggestions.
    :return: A list of suggestions as tuples.
    """
    if not user_input:
        return []

    user_str: str = ' '.join(user_input)
    suggestions: list = []
    if error_type == 'all':
        suggestions += match_first_word_mistaken_helper(user_input, user_str, data, 'add')
        if len(suggestions) < MAX_SUGGESTION:
            suggestions += match_first_word_mistaken_helper(user_input, user_str, data, 'replace')
        if len(suggestions) < MAX_SUGGESTION:
            suggestions += match_first_word_mistaken_helper(user_input, user_str, data, 'sub')
    else:
        suggestions += match_first_word_mistaken_helper(user_input, user_str, data, error_type)

    return remove_duplicates(suggestions)


def sort_and_filter_first_k(suggestions: List[List], k: int) -> List[List]:
    """
    Sort a list of suggestions by score from high to low and filter it, keeping the top k suggestions.

    :param suggestions: A list of suggestions as tuples.
    :param k: An integer representing the number of top suggestions to keep.
    :return: A list of the top k suggestions as tuples.
    """
    suggestions.sort(key=lambda x: (-x[3], x[0].lower()))
    return suggestions[:k]


def find_top_five_completions(user_input: List[str], data: FileData, ends_with_white_space: bool) -> List[List]:
    """
    Find the top five completions for the user's input based on data.

    :param ends_with_white_space: bool if the input ands with a white space.
    :param user_input: A list of strings representing the user's input.
    :param data: A FileData object containing data for suggestions.
    :return: A list of tuples representing the top five completions.
    """

    first_word: str = user_input[0]
    suggestions: List[List] = list()
    str_input: str = ' '.join(user_input)
    if len(user_input) == 1 and not ends_with_white_space:
        filtered_keys: List[str] = [key for key in data.words_graph.graph if key.startswith(str_input)]
        for key in filtered_keys:
            suggestions += find_match(str_input, data, key)
        [suggestion.append(len(str_input) * 2) for suggestion in suggestions]
        if len(suggestions) < MAX_SUGGESTION:
            suggestions += match_first_word_mistaken(user_input, data)
    else:
        if first_word in data.words_graph.graph:
            suggestions += find_match(str_input, data, first_word)
            [suggestion.append(len(str_input) * 2) for suggestion in suggestions]
            if len(suggestions) < MAX_SUGGESTION:
                new_suggestions: List[List] = find_mistaken_suggestions(str_input, data, first_word, len(suggestions))
                suggestions += new_suggestions
            if len(suggestions) < MAX_SUGGESTION and len(user_input[0]) < MAX_SUGGESTION:
                new_suggestions: List[List] = match_first_word_mistaken(user_input, data)
                suggestions += new_suggestions
        else:
            suggestions += match_first_word_mistaken(user_input, data)
    sorted_suggestions: List[List] = sort_and_filter_first_k(suggestions, MAX_SUGGESTION)
    [suggestion.pop(3) for suggestion in sorted_suggestions]
    return remove_duplicates(sorted_suggestions)


def find_alternative_words(word: str, error_type: str) -> Set[str]:
    """
    Generate alternative words by inserting, removing or replacing a space or a letter within a word.

    :param error_type: witch error to check
    :param word: A string representing the word for which alternative words are generated.
    :return: A set of alternative words.
    """

    alphabet: List[str] = list(string.ascii_lowercase)
    alphabet.append(' ')
    alternatives: Set[str] = set()

    for index in range(len(word) + 1):
        for letter in alphabet:
            if error_type == 'add':
                alternatives.add(word[:index] + letter + word[index:])
            elif error_type == 'replace':
                alternatives.add(word[:index] + letter + word[index + 1:])
            elif error_type == 'sub':
                alternatives.add(word[:index] + word[index + 1:])
            else:
                raise Exception('No such option')

    return alternatives - {word, ''}
