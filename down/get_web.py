#!/bin/env python
import urllib2
from w3lib.form import encode_multipart
from urlparse import urlparse, urljoin
import re

def pick_str(str, bs, es='"'):
    bslen = len(bs)
    a = str.find(bs)
    if a != -1:
        b = str.find(es, a+bslen)
        if b != -1:
            return str[a+bslen:b].strip()
    return ''

def fmt_text(str, level=2):
    str = str.strip().replace(',','%2C').replace('\n', '\\n')
    if level == 2:
        str = re.sub(r'/$', '', re.sub(r'&#\d+;?','',str.replace('&amp;','&').replace('&amp;','&')).strip())
    return str

url = 'http://www.taobao.com'
url = 'http://tds.alicdn.com/json/price_cut_data.htm?id=15432151888&rootCat=50013864&unicode=true&v=1'
out = 'web.htm'
response = urllib2.urlopen(url)
#open(out,'w').write(response.read())
body = response.read()
print body

line = []
for cat in body.split("person")[0].split("{name:")[1:]:
    c = cat.split('{x')
    try:
        name = eval("u" + c[0].split(',')[0])
    except:
        name = pick_str(c[0], "'","'")
    a = []
    for i in c[1:]:
        d = i.split(',')
        a.append("-".join([d[1].strip(), d[2], d[4].split(':')[1], pick_str(d[5],':',' ')]))
    line.append(name + ":" + "=".join(a))
print  fmt_text("#".join(line))

#print html
#print response.read()

'''
data = {
    'project': 'test',
    'para': '111:222:333:None,444:555:666',
}
if (True):
    data['priority'] = '3'

    body, boundary = encode_multipart(data)
    url = urljoin('http://www.baidu.com', 'addtask.json')
    headers = {
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
        'Content-Length': str(len(body)),
    }

req = urllib2.Request(url, body, headers)
print req.get_data()
'''


