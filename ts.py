# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def run():
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
    # headers = {
    #     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    #     'Accept - Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    #     'Connection': 'Keep-Alive',
    #     'Host': 'zhannei.baidu.com',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    # }
    r = requests.get('https://www.bishijie.com/coins/top/100', headers=headers)
    print(r.text)
if __name__ == '__main__':
    run()
