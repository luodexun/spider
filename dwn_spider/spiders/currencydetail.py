# -*- coding: utf-8 -*-
import scrapy,time,re
import pymysql
from scrapy import Request
from dwn_spider.items.currencydetail_item import CurrencydetailItem
from dwn_spider.settings import *

class CurrencydetailSpider(scrapy.Spider):
    def __init__(self, *a, **kw):
        super(CurrencydetailSpider, self).__init__(*a, **kw)
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                    db='shop',
                                    port=MYSQL_PORT, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.conn.ping(True)
        self.cur = self.conn.cursor()
    name = 'currencydetail'
    # 允许抓取的域名，可选
    # allowed_domains=['bishijie.com']
    start_urls = ['https://www.bishijie.com/coins/top/100']

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1,
        # "SPIDER_MIDDLEWARES": {
        #     'dwn_spider.middlewares.CrawlOnceMiddleware': 100,
        # },
        # "DOWNLOADER_MIDDLEWARES": {
            # 'dwn_spider.middlewares.CrawlOnceMiddleware': 50,
            # 'dwn_spider.middlewares.XdailiProxyMiddleware': 350,
            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        # },
        "ITEM_PIPELINES": {
            'dwn_spider.pipelines.currencydetail_pipeline.CurrencydetailPipeline': 300
        }
    }
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.bishijie.com/',
        'Host': 'www.bishijie.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def parse(self, response):
            self.cur.execute(
                """select DISTINCT currency_code,currency,currency_name,detail_url from w_currency_market """)
            res = self.cur.fetchall()
            for v in res:
                yield Request(v['detail_url'],meta={'currency_code': v['currency_code'], 'currency': v['currency'], 'currency_name': v['currency_name']},
                                     callback=self.parse_detail, headers=self.headers)
    def parse_detail(self, response):
        currency_code = response.meta['currency_code']
        currency = response.meta['currency']
        currency_name = response.meta['currency_name']

        update_time =int(time.time())
        Currencydetail = CurrencydetailItem()
        Currencydetail['currency_code'] = currency_code
        Currencydetail['currency'] = currency
        Currencydetail['currency_name'] = currency_name
        Currencydetail['englishname'] = response.xpath("//div[@class='main_info']/div[@class='left']/table/tbody/tr[2]/th[2]/text()").extract_first()
        Currencydetail['abbreviation'] = response.xpath("//div[@class='main_info']/div[@class='left']/table/tbody/tr[3]/th[2]/text()").extract_first()
        Currencydetail['release_time'] = response.xpath("//div[@class='main_info']/div[@class='left']/table/tbody/tr[4]/th[2]/text()").extract_first()
        if response.xpath("//div[@class='main_info']/div[@class='left']/p/text()").extract_first():
            Currencydetail['introduction'] = response.xpath("//div[@class='main_info']/div[@class='left']/p/text()").extract_first()
        else:
            Currencydetail['introduction'] = ''
        total_circulation = re.findall("\d+", response.xpath("//div[@class='cur_info_list']/p[2]/text()").extract_first())[0]
        Currencydetail['total_circulation'] = total_circulation
        total_issue_amount = re.findall("\d+", response.xpath("//div[@class='cur_info_list']/p[3]/text()").extract_first())[0]
        Currencydetail['total_issue_amount'] = total_issue_amount
        Currencydetail['update_time'] = update_time
        # print(Currencydetail)
        yield Currencydetail


