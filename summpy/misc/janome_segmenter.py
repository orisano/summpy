# coding: utf-8
from __future__ import unicode_literals

import re

from typing import *

from janome.tokenizer import Tokenizer, Token


tokenizer = Tokenizer()


def is_stopword(n):  # type: (Token) -> bool
    if len(n.surface) == 0:
        return True
    elif re.search(r'^[\s!-@\[-`\{-~　、-〜！-＠［-｀]+$', n.surface):
        return True
    elif re.search(r'^(接尾|非自立)', n.part_of_speech.split(',')[1]):
        return True
    elif 'サ変・スル' == n.infl_form or 'ある' == n.base_form:
        return True
    elif re.search(r'^(名詞|動詞|形容詞)', n.part_of_speech.split(',')[0]):
        return False
    else:
        return True


def not_stopword(n):  # type: (Token) -> bool
    return not is_stopword(n)


def node2word(n):  # type: (Token) -> Text
    return n.surface


def node2norm_word(n):  # type: (Token) -> Text
    if n.base_form != '*':
        return n.base_form
    else:
        return n.surface


def _decode_janome_token(t, encoding='utf-8'):  # type: (Token, Text) -> Token
    attributes = ('surface', 'base_form', 'part_of_speech', 'infl_form')
    for attr_name in attributes:
        value = getattr(t, attr_name)
        if type(value) == str:
            setattr(t, attr_name, value.decode('utf-8'))
    return t


def word_segmenter_ja(sent, node_filter=not_stopword, node2word=node2norm_word):
    # type: (Text, Callable[[Token], bool], Callable[[Token], Text]) -> List[Text]
    nodes = (_decode_janome_token(t) for t in tokenizer.tokenize(sent))

    if node_filter:
        nodes = [n for n in nodes if node_filter(n)]
    words = [node2word(n) for n in nodes]

    return words


if __name__ == '__main__':
    text = '今日はいい天気ですね。'
    print('|'.join(word_segmenter_ja(text)).encode('utf-8'))
