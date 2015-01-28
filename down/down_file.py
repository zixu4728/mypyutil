#!/bin/env
import urllib
import urllib2
#import requests
import sys

url = 'http://192.168.1.100/test.zip'
url = 'http://107.170.228.88:6801/items/comp_list/compressed.2014.12.25.13'

f = urllib.urlretrieve(url)
print f.read()
sys.exit(0)

# way 1
print "downloading with urllib"
urllib.urlretrieve(url, "code.zip")

# way 2
print "downloading with urllib2"
f = urllib2.urlopen(url)
data = f.read()
with open("code2.zip", "wb") as code:
    code.write(data)

# way 3
print "downloading with requests"
#r = requests.get(url)
#with open("code3.zip", "wb") as code:
#    code.write(r.content)
