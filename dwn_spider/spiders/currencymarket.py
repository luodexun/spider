# -*- coding: utf-8 -*-
import scrapy,time,pymysql
from scrapy import Request
from dwn_spider.items.currencymarket_item import CurrencymarketItem
from dwn_spider.settings import *

class CurrencymarketSpider(scrapy.Spider):
    def __init__(self, *a, **kw):
        super(CurrencymarketSpider, self).__init__(*a, **kw)
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                    db='test',
                                    port=MYSQL_PORT, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.conn.ping(True)
        self.cur = self.conn.cursor()
    name = 'currencymarket'
    # 允许抓
    # 取的域名，可选
    # allowed_domains=['bishijie.com']
    start_urls = ['https://www.bishijie.com/coins/top/all']
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
            'dwn_spider.pipelines.currencymarket_pipeline.CurrencymarketPipeline': 300
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

    def format_fiat(self, val):
        resval = ''
        if val >= 1:#10万及以上，取整
            if val >= 100000:
                resval = int(val)
            else:# 10万及以下，取2位小数
                resval = round(val,2)
        else:# 小于1的
            if val < 0.000001: #10万分之一以下的，用科学计数法显示
                resval = "%e" % val
            elif val < 0.001:
                resval = round(val,8)
            else: #普通的，保留8位小数
                resval = round(val,4)
        return resval

    def format_market_cap(self, val):
        resval = ''
        if val >= 1000000000:# 10亿以上，不保留小数
            resval = str(round(val / 100000000,0)) + "亿"
        elif val >= 100000000: # 1亿以上，到10亿，保留2位小数
            resval = str(round((val / 100000000),2)) + "亿"
        elif val >= 100000:# 十万以上，到1亿，不保留小数
            resval = str(round(val / 10000,0)) + "万"
        elif val >= 10000: # 1万以上，到10万保留4位小数；
            resval = str(round(val / 10000,4)) + "万"
        elif val >= 1000:
            resval = str(round(val, 0))
        else:
            resval = str(round(val, 2))
        return resval

    def parse(self, response):
        #删除一个小时之前的数据
        sql = """DELETE from w_currency_market where create_time < '{}' """.format(int(time.time()-3600))
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()

        currency_exchange_rates = response.xpath("//div[@id='currency-exchange-rates']/@data-cny").extract_first()
        node_list = response.xpath("//table[@id='coinTable']/tbody[@id='table_body']/tr")
        create_time =int(time.time())
        for node in node_list:
            Currencymarket = CurrencymarketItem()
            Currencymarket['currency_code'] = node.xpath("./td[@class='coinname']/a/@href").extract_first().split('/')[2]
            Currencymarket['currency_exchange_rates'] = currency_exchange_rates
            currency = node.xpath("./td[@class='coinname']/a/@title").extract_first().strip()
            Currencymarket['currency'] = currency.split('-')[0]
            Currencymarket['currency_name'] = currency.split('-')[1]
            Currencymarket['icon_url'] = node.xpath("./td[@class='coinname']//img/@src").extract_first()
            price_rmb = float(node.xpath("./td/a[@class='price']/text()").extract_first()) / float(currency_exchange_rates)
            Currencymarket['price_rmb'] = self.format_fiat(price_rmb)
            Currencymarket['price_usd'] = '{:.18f}'.format(float(node.xpath("./td/a[@class='price']/@data-usd").extract_first()))
            rise_rmb = node.xpath("./td/font/@data-usd").extract_first()
            Currencymarket['rise_rmb'] = str(round(float(rise_rmb),2))+'%'
            Currencymarket['rise_usd'] = '{:.18f}'.format(float(node.xpath("./td/font/@data-usd").extract_first()))
            volume_rmb = float(node.xpath("./td[@class='td_right volume']/text()").extract_first()) / float(currency_exchange_rates)
            Currencymarket['volume_rmb'] = self.format_market_cap(volume_rmb)
            Currencymarket['volume_usd'] = node.xpath("./td[@class='td_right volume']/@data-usd").extract_first()
            market_cap_rmb = float(node.xpath("./td[@class='td_right market_cap']/text()").extract_first()) / float(currency_exchange_rates)
            Currencymarket['market_cap_rmb'] = self.format_market_cap(market_cap_rmb)
            Currencymarket['market_cap_usd'] = node.xpath("./td[@class='td_right market_cap']/@data-usd").extract_first()
            Currencymarket['create_time'] = create_time
            Currencymarket['detail_url'] = 'https://www.bishijie.com'+node.xpath("./td[@class='coinname']/a/@href").extract_first()
            # print(Currencymarket)
            yield Currencymarket

            # Currencymarket['englishname'] = ''
            # Currencymarket['abbreviation'] = ''
            # Currencymarket['release_time'] = ''
            # Currencymarket['introduction'] = ''
            # Currencymarket['total_circulation'] = ''
            # Currencymarket['total_issue_amount'] = ''
