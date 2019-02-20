# -*- coding: utf-8 -*-
import pymysql.cursors
from dwn_spider.settings import *

class CurrencymarketPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            db='shop',
            charset=MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor)
        self.conn.ping(True)
        self.cur = self.conn.cursor()

    def open_spider(self, spider):
        print('我要开始了哦')

    def process_item(self, item, spider):
        try:
            insert_sql = """insert into w_currency_market (currency_exchange_rates,currency,currency_name,icon_url,price_rmb,
                            price_usd,rise_rmb,rise_usd,volume_rmb,volume_usd,
                            market_cap_rmb,market_cap_usd,detail_url,create_time,currency_code) 
                            value ('{}','{}','{}','{}','{}',
                            '{}','{}','{}','{}','{}',
                            '{}','{}','{}','{}','{}')""".format(item['currency_exchange_rates'], item['currency'], pymysql.escape_string(item['currency_name']), item['icon_url'], item['price_rmb'],
                                                           item['price_usd'],item['rise_rmb'],item['rise_usd'],item['volume_rmb'],item['volume_usd'],
                                                           item['market_cap_rmb'],item['market_cap_usd'],item['detail_url'],item['create_time'],item['currency_code'])
            # print(insert_sql)
            self.cur.execute(insert_sql)
            self.conn.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            raise error

        return item

    def close_spider(self, spider):
        self.conn.close()
        print('我结束了')
