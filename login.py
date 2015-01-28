from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.selector import Selector
import re
import urllib
import hashlib
import os
import datetime
import time

from scrapy.item import Item, Field
from scrapy.http import FormRequest

class LoginSpider(Spider):
    name = 'example'
    start_urls = ['https://login.taobao.com/member/login.jhtml?f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F']

    def parse(self, response):
        return [FormRequest.from_response(response,
            formdata={'username': 'shpudong2006@163.com', 'password': 'shpd123456'},
            callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            print "Login failed"
            self.log("Login failed", level=log.ERROR)
            return
        else:
            print "\n-----------------------------------------------------"
            print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOK"
            print "-----------------------------------------------------\n"
            print response.body
