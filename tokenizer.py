# coding: utf-8

import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value"])

def tokenizer(pat, text, ignore=['SPACE', ]):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        if m.lastgroup not in ignore:
            yield Token(m.lastgroup, m.group())

if __name__ == '__main__':
    expr = "( src in 10.0.0.0/24 & !(src = 10.0.0.1)) | (src in 127.0.0.0/8 | dst in 127.0.0.0/8)"
    SRC = r'(?P<SRC>src)'
    DST = r'(?P<DST>dst)'
    IN  = r'(?P<IN>in)'
    SYMBOL = r'(?P<SYMBOL>[&\|!]+)'
    NETWORK = r'(?P<NETWORK>\d{1,3}\.d{1,3}\.d{1,3}\.d{1,3}/\d{1,3})'
    IPADDR = r'(?P<IPADDR>\d{1,3}\.d{1,3}\.d{1,3}\.d{1,3})'
    EQ = r'(?P<EQ>=)'
    BRACKETS = r'(?P<BRACKETS>[\(\)]+)'
    SPACE = r'(?P<SPACE>\s+)'

    pat = re.compile("|".join([SRC, DST, IN, SYMBOL, NETWORK, IPADDR, EQ, BRACKETS, SPACE]))
    for t in tokenizer(pat, expr):
        print t
