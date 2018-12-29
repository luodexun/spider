# -*- coding: utf-8 -*-
import scrapy


class CurrencymarketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    currency_code = scrapy.Field()#币种唯一编码
    currency_exchange_rates = scrapy.Field()#货币汇率
    currency = scrapy.Field()#币种
    currency_name = scrapy.Field()#币种名字
    icon_url = scrapy.Field()#图标
    price_rmb =scrapy.Field()#RMB价格
    price_usd =scrapy.Field()#美元价格
    rise_rmb=scrapy.Field()#RMB涨幅
    rise_usd=scrapy.Field()#美元涨幅
    volume_rmb=scrapy.Field()#RMB24H交易量
    volume_usd=scrapy.Field()#美元24H交易量
    market_cap_rmb=scrapy.Field()#RMB市值
    market_cap_usd=scrapy.Field()#美元市值
    detail_url=scrapy.Field()#简介链接
    # englishname=scrapy.Field()#英文名
    # abbreviation=scrapy.Field()#简称
    # release_time=scrapy.Field()#发布时间
    # introduction=scrapy.Field()#简介
    # total_circulation=scrapy.Field()#流通总量
    # total_issue_amount=scrapy.Field()#发行总量
    create_time=scrapy.Field()
