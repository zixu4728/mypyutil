#-*- coding:utf-8 -*-
#!/bin/env python

import time
import datetime

days_lst = [u'\u4eca\u5929', u'\u6628\u5929', u'\u524d\u5929'] # today,yesterday,the day before yesterday
for da in range(1,8):
    dd = datetime.datetime.utcnow() + datetime.timedelta(hours=8) - datetime.timedelta(days=da)
    ndays_ago = u"%02d.%02d" % (dd.month, dd.day)
    days_lst.append(ndays_ago)

print days_lst
