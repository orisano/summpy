# coding: utf-8
from __future__ import unicode_literals

import os

from typing import *


def tree_encode(obj, encoding='utf-8'):
    # type: (Union[list, tuple, dict, Text], Text) -> Union[list, tuple, dict, bytes]
    if isinstance(obj, (list, tuple)):
        return [tree_encode(e, encoding) for e in obj]
    elif isinstance(obj, dict):
        return {tree_encode(k, encoding): tree_encode(v, encoding) for k, v in obj.items()}
    else:
        return obj.encode(encoding)


def sent_splitter_ja(text, delimiters=set('。．？！\n\r'), parenthesis='（）「」『』“”'):
    # type: (Text, Set[Text], Text) -> Generator[Text]
    """
    Args:
      text: unicode string that contains multiple Japanese sentences.
      delimiters: set() of sentence delimiter characters.
      parenthesis: to be checked its correspondence.
    Returns:
      generator that yields sentences.
    """
    paren_chars = set(parenthesis)
    close2open = dict(zip(parenthesis[1::2], parenthesis[0::2]))
    pstack = []
    buff = []

    for i, c in enumerate(text):
        c_next = text[i+1] if i+1 < len(text) else None
        # check correspondence of parenthesis
        if c in paren_chars:
            if c in close2open:  # close
                if len(pstack) > 0 and pstack[-1] == close2open[c]:
                    pstack.pop()
            else:  # open
                pstack.append(c)

        buff.append(c)
        if c in delimiters:
            if len(pstack) == 0 and c_next not in delimiters:
                yield ''.join(buff)
                buff = []

    if len(buff) > 0:
        yield ''.join(buff)


if os.getenv("SUMMPY_USE_JANOME"):
    from .misc.janome_segmenter import word_segmenter_ja
else:
    try:
        from .misc.mecab_segmenter import word_segmenter_ja
    except ImportError:
        from .misc.janome_segmenter import word_segmenter_ja


if __name__ == '__main__':
    pass
