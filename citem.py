from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.downloader import Downloader, Slot
from scrapy.item import Item, Field
from scrapy import signals
from scrapy import log
import re
import os
import datetime
import time
import json

import sys
reload( sys )
sys.setdefaultencoding('utf-8')

class BaoItem(Item):
    shop = Field()
    shopid = Field()
    itemid = Field()
    image = Field()
    title = Field()
    ori_price = Field()
    price = Field()
    mprice = Field()
    amount_all = Field()
    amount_30 = Field()
    rate = Field()
    dsr = Field()
    favor = Field()
    cat_id = Field()
    brand = Field()
    start = Field()
    end = Field()
    promo = Field()

    #for offer
    user = Field()
    rank = Field()
    amount = Field()
    chargetime = Field()
    main = Field()

def pick_str(str, bs, es='"'):
    bslen = len(bs)
    a = str.find(bs)
    if a != -1:
        b = str.find(es, a+bslen)
        if b != -1:
            return str[a+bslen:b]
    return ''

def pick_xpath(sel, path):
    value = sel.xpath(path).extract()
    if value and value[0].strip():
        return value[0].strip()
    return ''

def fmt_text(str, level=2):
    str = str.replace(',','%2C').replace('\n', '\\n')
    if level == 2:
        str = re.sub(r'/$', '', re.sub(r'&#\d+;?','',str.replace('&amp;','&').replace('&amp;','&')).strip())
    return str

class ProductSpider(Spider):
    name = "cproduct"
    #download_delay = 4

    start_urls = ['http://www.taobao.com']
    para = ''
    delay = ''

    def __init__(self, para=None, delay=220000, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.stats_spider_closed, signal=signals.stats_spider_closed)
        dispatcher.connect(self.engine_opened, signal=signals.engine_started)

        if (para is not None):
            self.para = para
        self.delay = int(delay)
        #for i in para.split(","):
        #    self.start_urls.append("http://item.taobao.com/item.htm?id=%s" % i)

    def engine_opened(self):
        log.msg('para:' + self.para)
        self.crawler.engine.downloader.slots['s.taobao.com'] = Slot(1, 1, self.settings)
        self.crawler.engine.downloader.slots['detailskip.taobao.com'] = Slot(5, 0.1, self.settings)
        self.crawler.engine.downloader.slots['count.tbcdn.cn'] = Slot(5, 0.1, self.settings)

    def stats_spider_closed(self, spider, spider_stats):
        print "STAT ITEM_COUNT:%d,REQUEST_COUNT:%d,RESPONSE_COUNT:%d,RESPONSE_302:%d" % (
            spider_stats['item_scraped_count'] if 'item_scraped_count' in spider_stats else 0,
            spider_stats['downloader/request_count'] if 'request_count' in spider_stats else 0,
            spider_stats['downloader/response_count'] if 'downloader/response_count' in spider_stats else 0,
            spider_stats['downloader/response_status_count/302'] if 'downloader/response_status_count/302' in spider_stats else 0)

    def parse(self, response):
        if not self.para:
            raise Exception('No have para!')
    
        for line in self.para.split(','):
            a = line.split(':')
            
            shopid = a[0]
            sellerid = a[1]
            total = int(a[2])

            delay = self.delay 
            #if len(a) >= 4 and a[3] and a[3] != 'None':
            #    delay = int((datetime.datetime.utcnow() + datetime.timedelta(hours=8) - datetime.datetime.utcfromtimestamp(int(a[3]) - 4*3600)).total_seconds())
            log.msg('shopid:%s,delay:%d' % (shopid, delay))

            num = 300
            cnt = (total)/num
            if (total)%num != 0:
                cnt += 1
            n = 0
            for i in range(cnt+1):
                url = 'http://223.5.23.134:8983/solr/item/select?q=shopid%3A'+shopid+'&sort=amount1+desc&start='+str(n)+'&rows='+str(num)+'&wt=json'
                yield Request(url, meta={'shopid':shopid, 'delay':delay}, callback=self.parse_item_s)
                n += num

    def parse_item_s(self, response):
        shopid = response.meta['shopid']
        delay  = response.meta['delay']

        #print '-'*5+response.url
        items = json.loads(response.body)
        for i in items['response']['docs']:
            l = BaoItem()
            l['itemid'] = i['itemid']
            l['shopid'] = shopid

            itemurl = 'http://item.taobao.com/item.htm?id=' + str(i['itemid'])
            yield Request(itemurl, meta={'item':l, 'delay':delay}, callback=self.parse_item)

    def parse_item(self, response):
        #log.msg("item req:\t" + response.url)
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        l = response.meta['item'] 
        delay = response.meta['delay']

        # item id
        #m = re.match(r'.*[?&](?:item_?)?id=(\d+).*', response.url)
        #l["itemid"] = m.group(1) 

        # product category id
        cat_id = pick_str(response.body, 'category=item%5f', '&')
        if not cat_id:
            cat_id = 0
        l["cat_id"] = cat_id

        # shop id
        #shopid = pick_str(response.body, 'shopId:"')
        #if not shopid:
        #    shopid = 0
        #    log.err('Not found shopid [%s]' % (response.url))
        #l["shopid"] = shopid

        sel = Selector(response)

        # shop name
        shop = pick_xpath(sel, "//div[@class='tb-shop-name']//a/@title")
        l["shop"] = shop.replace(',','%2C')

        # product image
        image = pick_xpath(sel, "//div[contains(@class,'tb-booth')]//img/@data-src")
        if image:
            image = image[:image.rfind("_")]
        l["image"] = image

        # product brand
        brand = ""
        attrs = sel.xpath("//ul[@class='attributes-list']/li/text()").extract()
        for attr in attrs:
            if (attr.find(u'\u54c1\u724c') == 0):
                brand = attr.split(":")[1].strip()
        l["brand"] = fmt_text(brand.strip())

        # product marked price 
        ori_price = pick_xpath(sel, "//em[@class='tb-rmb-num']/text()")
        if not ori_price:
            ori_price = '0'
        l['ori_price'] = ori_price.split('-')[0].strip() 

        # product title
        title = pick_xpath(sel, '//h3[@class="tb-main-title"]/text()') or pick_xpath(sel, '//h3[@class="tb-item-title"]/text()') 
        l["title"] = fmt_text(title)

        # product price
        l['mprice'] = '0'
        ajax_price = pick_str(response.body, '"wholeSibUrl":"')
        if ajax_price:
            yield Request(ajax_price, meta={'item':l}, callback=self.parse_price_ajax)
        else:
            l['price'] = '0'
            log.msg("Not found price [shopid:%s,%s]" % (l['shopid'], response.url))

        # product amount
        amount = pick_str(response.body, '"apiItemInfo":"')
        if amount:
            amount = amount + '&callback=DT.mods.SKU.GetItemInfo.fire'
            yield Request(amount, meta={'item':l, 'download_slot':'amount'}, callback=self.parse_amount_ajax)
        else:
            l['amount_30'] = '0'

        # product promo
        promo = pick_xpath(sel, '//*[@id="Ul_promo"]/li/a/text()')
        if promo:
            l['promo'] = promo.replace(':','').strip()
        """else:
            promo = pick_str(response.body, '"wholeSibUrl":"')
            if promo:
                yield Request(promo, meta={'item':l}, callback=self.parse_promo_ajax)
            else:
                l['promo'] = 'normal' """

        # product rate
        rate = pick_str(response.body, 'rateCounterApi:"')
        if rate:
            rate = rate + '&callback=json58'
            yield Request(rate, meta={'item':l}, callback=self.parse_rate_ajax)     
        else:
            l['rate'] = '0'

        # product favor
        favor = pick_str(response.body, 'counterApi:"')
        if favor:
            favor = favor + '&callback=DT.mods.SKU.CountCenter.saveCounts'
            yield Request(favor, meta={'item':l}, callback=self.parse_favor_ajax)     
        else:
            l['favor'] = '0'

        #get item order
        req = "http://www.taobao.com"
        deal = pick_str(response.body, 'data-api="')
        if deal:
            deal_ajax_url = deal + '&callback=Hub.data.records_reload'
            req = deal_ajax_url
            meta = {'shopid':l['shopid'], 'itemid':l['itemid'], 'pageid':'1', 'delay':delay}
            yield Request(deal_ajax_url, meta=meta, callback=self.parse_ajax_offer)
        else:
            deal = pick_str(response.body, 'buyerRecordUrl: "')
            if deal:
                deal_ajax_url = deal + '&callback=jsonp238'
                req = deal_ajax_url
                meta = {'shopid':l['shopid'], 'itemid':l['itemid'], 'pageid':'1', 'delay':delay}
                yield Request(deal_ajax_url, meta=meta, callback=self.parse_ajax_offer)

        [starts, ends, soldTotalNum, totalSQ] = [0, 0, 0, 0]
        if (req != "http://www.tmall.com"):
            m = re.match(r'.*[?&]starts=(\d+).*', req)
            if (m):
                starts = m.group(1)
            else:
                print "starts", req
            m = re.match(r'.*[?&]ends=(\d+).*', req)
            if m:
                ends = m.group(1)

        l["amount_all"] = 0 
        l["start"] = starts
        l["end"] = ends

        if ('price' in l and 'amount_30' in l and 'rate' in l and 'favor' in l):
            yield l
                
    def parse_price_ajax(self, response):
        #print '+'*5 + ' ' + 'price_ajax_url: ' + response.url + ' ' + '+'*5
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        price = pick_str(response.body, 'price:"')

        item = response.meta['item']
        if price and price.strip():
            item['price'] = price.strip()
        else:
            item['price'] = item["ori_price"]

        if 'promo' not in item:
            promtype = ''
            str = pick_str(response.body, 'g_config.PromoData=', '}')
            if str:
                promtype = re.search(r'type:\s*"([^"]+)', str)
                if promtype and promtype.group(1).strip():
                    promtype = promtype.group(1).strip().decode('gbk')
                else:
                    promtype = re.search(r'<div class="tb-purchase-not-allowed">([^<]+)<a href="http://ju.taobao.com', response.body)
                    if promtype and promtype.group(1).strip():
                        promtype = promtype.group(1).strip().replace('\xbb\xee\xb6\xaf\xc9\xcc\xc6\xb7\xa3\xac','').decode('gbk')
            item['promo'] = promtype
        
        if ('rate' in item and 'amount_30' in item and 'favor' in item):
            return item

    def parse_amount_ajax(self, response):
        #print '+'*20 + "amount_ajax_url: " + response.url
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        amount = re.search(r'quanity: (\d+)', response.body)

        item = response.meta['item']
        if amount and amount.group(1).strip():
            item['amount_30'] = amount.group(1).strip()
        else:
            item['amount_30'] = 0

        if ('rate' in item and 'price' in item and 'favor' in item):
            return item

    def parse_favor_ajax(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        favor = re.search(r'ICCP_[^:]+:(\d+)', response.body)

        item = response.meta['item']
        if favor and favor.group(1).strip():
            item['favor'] = favor.group(1).strip()
        else:
            item['favor'] = 0
        
        if ('rate' in item and 'price' in item and 'amount_30' in item):
            return item

    def parse_rate_ajax(self, response):
        #print '+'*5 + ' ' + response.url +  ' ' + '+'*5
        #from scrapy.shell import inspect_response
        #inspect_response(response)
        
        item = response.meta['item']
        rate = re.search(r'ICE_3_feedcount-[^:]+:(\d+)', response.body)
        if rate:
            item['rate'] = rate.group(1).strip()
        else:
            item['rate'] = 0

        if ('favor' in item and 'price' in item and 'amount_30' in item):
            return item

    def parse_ajax_offer(self, response):
        if ("redirect_urls" in response.meta):
            log.msg("MDSKIP ERROR: "+response.url)
            print response.meta
            return

        #print '+'*5 + ' deal_ajax_url:' + response.url
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        pageid = response.meta['pageid']
        shopid = response.meta['shopid']
        itemid = response.meta['itemid']
        delay  = response.meta['delay']

        #get json to html
        htmlstr = response.body[response.body.find('html:"')+6:response.body.find('",type:')]
        sel = Selector(text=htmlstr.replace('\\"','"').decode('GBK'), type="html")

        chargetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=8) 
        delay =220000

        trs= sel.xpath('//tr')
        for tr in trs[1:]:
            ct = tr.xpath('./td[4]/text()').extract()
            if (not ct):
                continue
            chargetime = ct[0]
            delta = dt - datetime.datetime.strptime(chargetime, "%Y-%m-%d %H:%M:%S")
            if (delta.total_seconds() > delay + 86400):
                break

            if (delta.total_seconds() > delay):
                continue 

            l = BaoItem()
            l['shopid'] = shopid
            l['itemid'] = itemid

            user = tr.xpath('./td[1]').extract()[0]
            l['user'] = re.sub(r'<[^>]*>', '', user).strip()

            rank = tr.xpath('./td[1]//img/@title').extract() or [""]
            l['rank'] = rank[0][:-7]

            price = tr.xpath('./td[2]/em[2]/text()').extract() or [""]
            l['price'] = price[0]

            amount = tr.xpath('./td[3]/text()').extract()
            if amount:
                l['amount'] = amount[0]
            else:
                continue

            sku = tr.xpath('./td[5]/div/p/text()').extract()
            l['main'] = ';'.join(sku).replace(",", "%2C")

            l['chargetime'] = chargetime
            yield l

        if 'redundant' in response.meta:
            return

        req = sel.xpath("//a[span]/@href").extract()
        if (req is not None and len(req) > 0):
            item = re.match(r'.*bidPage=(\d+).*', req[-1]) or re.match(r'.*bid_page=(\d+).*', req[-1])
            delta = dt - datetime.datetime.strptime(chargetime, "%Y-%m-%d %H:%M:%S")
            if (item is not None and delta.total_seconds() < delay):
                id = item.group(1)
                meta = {'shopid':shopid,'itemid':itemid,'pageid':id, 'delay':delay}
                yield Request(req[-1]+"&callback=jsonp1814",meta=meta,callback=self.parse_ajax_offer)

            if ('redundant' not in response.meta and item is not None and delta.total_seconds() >= delay):
                id = item.group(1)
                meta = {'shopid':shopid,'itemid':itemid,'pageid':id, 'redundant':True, 'delay':delay}
                yield Request(req[-1]+"&callback=jsonp1814",meta=meta,callback=self.parse_ajax_offer)

