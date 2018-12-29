# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import time

from scrapy import signals
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.utils.project import data_path
from scrapy.utils.request import request_fingerprint
from sqlitedict import SqliteDict

logger = logging.getLogger(__name__)
from dwn_spider.settings import XDL_ORDERNO,XDL_SECRET

class CrawlOnceMiddleware(object):
    def __init__(self, path, stats, default):
        self.path = path
        self.stats = stats
        self.default = default

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool('CRAWL_ONCE_ENABLED', True):
            raise NotConfigured()
        path = data_path(s.get('CRAWL_ONCE_PATH', 'crawl_once'),
                         createdir=True)
        default = s.getbool('CRAWL_ONCE_DEFAULT', default=False)
        o = cls(path, crawler.stats, default)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.db, dbpath = self._spider_db(spider)
        num_records = len(self.db)
        logger.info("Opened crawl database %r with %d existing records" % (
            dbpath, num_records
        ))
        self.stats.set_value('crawl_once/initial', num_records)

    def spider_closed(self, spider):
        self.db.close()

    def _spider_db(self, spider):
        dbpath = os.path.join(self.path, '%s.sqlite' % spider.name)
        db = SqliteDict(
            filename=dbpath,
            tablename='requests',
            autocommit=True,
        )
        return db, dbpath

    def _get_key(self, request):
        return (request.meta.get('crawl_once_key') or
                request_fingerprint(request))

    # spider middleware interface
    def process_spider_output(self, response, result, spider):
        for r in result:
            yield r

        # response is crawled, store its fingerprint in DB if crawl_once
        # is requested.
        if response.meta.get('crawl_once', self.default):
            key = self._get_key(response.request)
            self.db[key] = response.meta.get('crawl_once_value', time.time())
            self.stats.inc_value('crawl_once/stored')

    # downloader middleware interface
    def process_request(self, request, spider):
        if not request.meta.get('crawl_once', self.default):
            return
        if self._get_key(request) in self.db:
            self.stats.inc_value('crawl_once/ignored')
            raise IgnoreRequest()

orderno = XDL_ORDERNO
secret = XDL_SECRET
timestamp = int(time.time())
md5 = hashlib.md5()
md5.update(bytes('orderno={0},secret={1},timestamp={2}'.format(orderno, secret, timestamp), encoding='utf-8'))
sign = md5.hexdigest().upper()


class XdailiProxyMiddleware(object):
    # 讯代理
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://forward.xdaili.cn:80"
        request.headers['Proxy-Authorization'] = 'sign={0}&orderno={1}&timestamp={2}'.format(sign, orderno, timestamp)
