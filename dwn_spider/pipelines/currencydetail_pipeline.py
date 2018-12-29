# -*- coding: utf-8 -*-
import pymysql.cursors
from dwn_spider.settings import *

class CurrencydetailPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            db='test',
            charset=MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor)
        self.conn.ping(True)
        self.cur = self.conn.cursor()

    def open_spider(self, spider):
        print('我要开始了哦')

    def process_item(self, item, spider):
        try:
            insert_sql = """insert into w_currency_detail (currency_code,currency,currency_name,englishname,abbreviation,
                            release_time,introduction,total_circulation,total_issue_amount,update_time) 
                            value ('{}','{}','{}','{}','{}',
                            '{}','{}','{}','{}','{}')
                             ON DUPLICATE KEY UPDATE total_circulation='{}',total_issue_amount='{}',update_time='{}';""".format(item['currency_code'], item['currency'], pymysql.escape_string(item['currency_name']), pymysql.escape_string(item['englishname']), pymysql.escape_string(item['abbreviation']),
                                                           item['release_time'],pymysql.escape_string(item['introduction']),item['total_circulation'],item['total_issue_amount'],item['update_time'],item['total_circulation'],item['total_issue_amount'],item['update_time'])
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
