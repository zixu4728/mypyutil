#!/bin/env python

import re
import sys
import json
import MySQLdb
import time
import random

def select_mysql():
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='scrapy',passwd='123456',charset='utf8')
        conn.select_db('maijiainfo')
        cur = conn.cursor()

        count = cur.execute('select * from student where id=%s', (11,))
        print 'there has %s rows record' % count
        results = cur.fetchall() # ((v1,v2,...),(v1,v2,...),)
        print results
    
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
all_items = ['aa','bb','cc','dd']
def insert_mysql():
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='scrapy',passwd='123456',charset='utf8')
        conn.select_db('maijiainfo')
        cur = conn.cursor()

        vals = []
        for i in all_items:
            para = (int(time.time())+random.randint(10,100),i+'_'+str(random.randint(10,100)), random.randint(10,100))
            vals.append(para)

        print vals
        cur.executemany('insert into student (id,name,age) values (%s,%s,%s)', vals)
    
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

select_mysql()
#insert_mysql()
