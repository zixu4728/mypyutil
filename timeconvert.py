#!/bin/env python
import time
import sys

def str2secs(str):
    return int(time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S")))

def secs2str(secs):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(secs)))

if __name__ == '__main__':
    
    print sys.argv
    str = '2014-09-12 23:12:15'
    secs= 1420612284
    if len(sys.argv) > 1:
        secs = int(sys.argv[1])
    print (secs2str(secs))

    #print str2secs(secs2str(secs))
    #print secs2str(str2secs(str))

