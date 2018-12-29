# -*- coding: utf-8 -*-
import scrapy


class CurrencydetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    currency_code = scrapy.Field()#币种唯一编码
    currency = scrapy.Field()#币种
    currency_name = scrapy.Field()#币种名字
    englishname=scrapy.Field()#英文名
    abbreviation=scrapy.Field()#简称
    release_time=scrapy.Field()#发布时间
    introduction=scrapy.Field()#简介
    total_circulation=scrapy.Field()#流通总量
    total_issue_amount=scrapy.Field()#发行总量
    update_time=scrapy.Field()
