import pytest
from util import remove_punctuation_util

# test file for remove_punctuation_util.py

SENTENCE_01 = "H@@{%,i t#(he*re+, {have] y_o_u e~ve!!!r) s<=>ee<<n #a# w,h.a.l.e"
SENTENCE_02 = "Hi there have you ever seen a whale"
SENTENCE_02_WITH_SPACES = "Hi    there   have    you    ever    seen    a    whale    "


def test_remove_punctuation():
    assert remove_punctuation_util.remove_punctuation_from_sentence(
        SENTENCE_02) == "Hi there have you ever seen a whale"


def test_remove_white_spaces():
    assert " ".join(remove_punctuation_util.remove_extra_white_spaces(SENTENCE_02_WITH_SPACES)) == SENTENCE_02
    assert remove_punctuation_util.remove_extra_white_spaces(
        SENTENCE_02) == remove_punctuation_util.remove_extra_white_spaces(
        SENTENCE_02_WITH_SPACES)


def test_process_sentence():
    assert remove_punctuation_util.process_sentence(SENTENCE_01) == ['Hi', 'there', 'have', 'you',
                                                                     'ever', 'seen', 'a', 'whale']


pytest.main(['-v'])
