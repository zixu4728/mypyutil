#!/bin/env python

import time
import re

'''
f =  open('htm2','r')
str = f.read()
f.close()
print len(str)

def pick_str(str, bs, es='"'):
    bslen = len(bs)
    a = str.find(bs)
    if a != -1:
        b = str.find(es, a+bslen)
        if b != -1:
            return str[a+bslen:b]
    return ''

beg = time.time()
m = re.search(r'yjytest:"([^"]+)',str)
if m:
    print m.group(1)
end = time.time()
print end-beg

beg = time.time()
print pick_str(str, 'yjytest:"')
end = time.time()
print end-beg
'''


lst=['http://game.taobao.com/item.htm?item_num=40238857015',
   'http://paimai.taobao.com/json/show_bid_list.htm?current_page=1&page_size=15&item_id=36419175724',
   'http://dd.taobao.com/detail.htm?localstoreId=848fb79740cd4cef869a8554184293a2&itemId=38472200764',
   'http://waimai.taobao.com/item.htm?id=39681603833',
   'http://bang.taobao.com/item.htm?id=38923567713',
   'http://kezhan.trip.taobao.com/item.htm?item_id=39086798599&mt=&mt=']

dis_pat = re.compile(r'http://(game|waimai|paimai|dd|bang|trip|kezhan\.trip)\.taobao\.com')
def is_discard_url(url):
    m = re.search(dis_pat, url)
    return True if m else False

beg = time.time()
for s in lst:
    if (s.find('http://game.taobao.com') != -1 or s.find('http://paimai.taobao.com') != -1
        or s.find('http://dd.taobao.com/detail.htm') != -1 or s.find('http://waimai.taobao.com') != -1
        or s.find('http://bang.taobao.com') != -1 or s.find('http://kezhan.trip.taobao.com') != -1):
        print 'S0K'
end = time.time()
print 'STR:', end-beg

beg = time.time()
for s in lst:
    if not is_discard_url(s):
        print 'NOO'
end = time.time()
print 'REG:', end-beg

