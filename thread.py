#!/bin/env python
import thread
import time

#'''
sum = 1000

def test(sum):
    for i in xrange(1,1000):
        print sum,
        sum -= 1
        #time.sleep(1)

thread.start_new_thread(test,(sum,))
time.sleep(1)
thread.start_new_thread(test,(sum,))
#'''

'''
def Thread_test(i):
    print "hello",i

if __name__ == '__main__':
    for i in range(11):
        thread.start_new_thread(Thread_test,(i,))
        time.sleep(1)
'''
