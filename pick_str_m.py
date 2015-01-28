#!/bin/env python

import time
import re

str =  open('htm2','r').read()
str = 'asdfdsadfs'
print len(str)

def pick_str_m(str, blimit, elimit='"'):
    lst = []

    blen = len(blimit)
    beg = str.find(blimit)
    while beg != -1:
        end = str.find(elimit, beg+blen)
        if end != -1:
            lst.append(str[beg+blen:end])
            beg = str.find(blimit, end+1)
        else:
            lst.append(str[beg+blen:])
            beg = -1

    return lst 

beg = time.time()
ids = re.findall(r'"nid":"(\d+)"', str)
print ids 
end = time.time()
print 're:', end-beg

beg = time.time()
print pick_str_m(str, '"nid":"')
end = time.time()
print 'sb:', end-beg





