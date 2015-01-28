#!/usr/bin/python
s = ['   ','aa','  ', '   cccc ']

def filter_list(lst):
    newlst = []
    for i in lst:
        name = i.strip()
        if len(name) != 0:
            newlst.insert(0,name)
    return newlst
s = filter_list(s)
print s
        

