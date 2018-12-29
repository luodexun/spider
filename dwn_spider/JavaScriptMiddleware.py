# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import requests
from scrapy.downloadermiddlewares.stats import DownloaderStats

global driver
# driver = webdriver.PhantomJS()  # 指定使用的浏览器，写在此处而不写在类中，是为了不每次调用都生成一个信息独享，减少内存使用
option = webdriver.ChromeOptions()
# option.add_argument("--start-maximized")
# option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)
print("PhantomJS is starting...")


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        global driver
        url = request.url
        driver.get(url)
        # js = "var q=document.documentElement.scrollTop=10000"
        # driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        # time.sleep(3)

        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
        # headers = {'User-Agent': user_agent}
        # r = requests.post(url, headers=headers)
        text = [x.text for x in driver.find_elements_by_xpath("//table[@id='coinTable']/tbody[@id='table_body']/tr")]
        # print(driver.find_elements_by_xpath("//table[@id='coinTable']/tbody[@id='table_body']/tr").text)
        print(text)
        # body = driver.find_elements_by_xpath('/html')
        # print("访问" + r.text)
        # print("访问" + request.url)
        driver.quit()
        return HtmlResponse(url, encoding='utf-8', status=200,
                            # body=body
                            )
