from string import punctuation
from typing import List


# util file to process sentences (removes punctuation and extra white spaces from a string)

def remove_punctuation_from_sentence(sentence: str) -> str:
    return sentence.translate(str.maketrans('', '', punctuation)).lower()


def remove_extra_white_spaces(sentence: str) -> List[str]:
    return sentence.split()


def process_sentence(sentence: str) -> List[str]:
    return remove_extra_white_spaces(remove_punctuation_from_sentence(sentence))
