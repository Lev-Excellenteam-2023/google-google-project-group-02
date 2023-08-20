from string import punctuation
from typing import List


def remove_punctuation_from_sentence(sentence: str) -> str:
    return sentence.translate(str.maketrans('', '', punctuation))


def remove_extra_white_spaces(sentence: str) -> List[str]:
    return sentence.split()


def prepare_sentence_for_processing(sentence: str) -> List[str]:
    return remove_extra_white_spaces(remove_punctuation_from_sentence(sentence))
