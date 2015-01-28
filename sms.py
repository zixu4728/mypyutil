# -*- coding:utf-8 -*-
#!/bin/env python

import sys
import httplib
import urllib
import re
import time
import json
from optparse import OptionParser

red    = '\033[1;31m'
green  = '\033[1;32m'
yellow = '\033[1;33m'
c_end  = '\033[1;m'

def parse_opts():
    parser = OptionParser(usage="%prog [options] <message>", description="Send Fetion Message")
    parser.add_option("-p", "--phone", default="13701792664", help="the phone which will be send")
    return parser.parse_args()

class Fetion:
    url = "https://quanapi.sinaapp.com/fetion.php?u="

    def SendMsg(self, toTel, msg, fromTel='13701792664', pwd='kevin060522'):
        url = '%s%s&p=%s&to=%s&m=%s' % (self.url, fromTel, pwd, toTel, re.sub(" ", "%20", str(msg)))

        answer = urllib.urlopen(url)

        try:
            jdata = json.loads(answer.read())
            if jdata['result']==0:
                print '%sTo %s, Send success,msg:[%s]%s' % (green, toTel, msg, c_end)
                return True
            else:
                print '%sFail: %s%s' % (red, jdata["message"].encode("UTF-8"), c_end)
                return False
        except:
            print '%sSend Fail! SMS WebSite Fault!%s' % (red, c_end)
            return False
 
def main():
    opts, args = parse_opts()
    toTel = opts.phone
    if not args:
        print '    %susage: python %s -p <phonenumber> <message...>%s' % (red, sys.argv[0],c_end)
    else:
        print args
        Fetion().SendMsg(toTel, ' '.join(args))

if __name__ == '__main__':
    main()

    #ff = Fetion()
    #ff.SendMsg('13701792664', 'test test test 1111')
