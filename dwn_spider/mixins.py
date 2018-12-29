# -*- coding: utf-8 -*-
import re
import urllib
from urllib.parse import urlparse


class SpiderMixin(object):
    @staticmethod
    def format_cookie(str):
        """cookie字符串转字典"""
        cookies = {}
        for l in str.split(';'):
            (k, v) = re.findall(r'(.*?)=(.*)', l)[0]
            cookies[k.strip()] = v.strip()
        return cookies

    @staticmethod
    def parse_domain(url):
        return urlparse(url).netloc
