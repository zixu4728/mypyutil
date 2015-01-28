#!/bin/env python
import sys
import os
import time
import datetime
import urllib2
import json
import MySQLdb
from optparse import OptionParser
from urlparse import urlparse, urljoin
from w3lib.form import encode_multipart

def _sql(sql):
    kw = []
    try:
        conn=MySQLdb.connect(host='192.168.1.160',user='scrapy',passwd='LacQsRm4Miz9x',charset='utf8')
        cur=conn.cursor()
        conn.select_db('scrapy')
        count=cur.execute(sql)
        print 'there has %s rows record' % count
        results=cur.fetchall() # ((v1,v2,...),(v1,v2,...),)
        for r in results:
            kw.append(urllib2.quote(r[0].encode('GBK')))

        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #return kw
    print kw

def main():
    sql = 'select name from shop_task'
    _sql(sql)

if __name__ == "__main__":
    main()
