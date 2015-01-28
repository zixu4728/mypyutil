# -*- coding: utf-8 -*-
#!/bin/env python

import os

def test1(rootDir): 
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        #for d in dirs: 
        #    print os.path.join(root, d)      
        #for f in files: 
        #    print os.path.join(root, f) 
        print '-'*100
        print root, dirs, files
        #print '-- root --', root
        #print '-- dirs --', dirs
        #print '-- files--', files
        #print ''

def test2(rootDir): 
    print os.listdir(rootDir)
    return
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        print path 
        if os.path.isdir(path): 
            test2(path)

dir = "/home/scrapy/cshop"

test1(dir)
print '+'*100
#test2(dir)
