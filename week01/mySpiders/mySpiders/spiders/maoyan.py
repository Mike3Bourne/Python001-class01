#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maoyan.py
@Time    :   2020/06/28 03:38:17
@Author  :   Mike
@Contact :   bixshds@163.com
@Department   :  
@Desc    :   极客大学Python训练营课程1_作业2_v1.2：
            1. 作业题目：
            使用 Scrapy 框架和 XPath 抓取猫眼电影的前 10 个电影名称、电影类型和上映时间，
            并以 UTF-8 字符集保存到 csv 格式的文件中。
            2. 处理步骤：
            此为v1.2版本：使用了Scrapy框架
'''

# here put the import lib(scrapy、BeautifulSoup、MyspidersItem)
import scrapy
from bs4 import BeautifulSoup as bs
from mySpiders.items import MyspidersItem



class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films']

    def start_requests(self):
        # 获取是个电影的信息，无需翻页，所以暂时不使用for in 迭代
        cookies = {'__mta': '19125639.1593093704429.1593223600946.1593272111104.19', 'uuid_n_v': 'v1', 'uuid': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', '_lxsdk_cuid': '172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8', '_lxsdk': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', 'mojo-uuid': 'e1772807c81f11b610e103c16996314e',
                   '_csrf': '0fce7216759568c83b3097bf466cb9105aae2480e9248fcdd8c9a1c941c54800', 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1593174407,1593175457,1593187363,1593223570', 'mojo-session-id': '{"id":"38f0e36fe7f72e41d683cef66a682575","time":1593271559357}', 'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1593272111', 'mojo-trace-id': '8', '_lxsdk_s': '172f662a543-dca-5d6-18b%7C%7C11'}
        
        url = 'http://maoyan.com/films?showType=3&sortId=1'
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    # def parse(self, response):
    #     pass

    def parse(self, response):
        bs_info = bs(response.text, 'html.parser')
        url_list = bs_info.find_all(
            'div', attrs={'class': 'channel-detail movie-item-title'})
        for i in url_list:
            item = MyspidersItem()
            film_url = 'https://maoyan.com' + i.find('a').get('href')
            item['film_url'] = film_url
            yield scrapy.Request(url=film_url, meta={'item':item}, callback=self.parse2)
            if url_list.index(i) > 10:
                break

    def parse2(self, response):
        item = response.meta['item']
        bs2_info = bs(response.text, 'html.parser')

        film_name = bs2_info.find('h1').get_text()
        item['film_name'] = film_name

        filme_type = ''
        for atag in bs2_info.find('div', attrs={'class': 'movie-brief-container'}).find_all('a'):
            filme_type = filme_type + atag.text.lstrip()
        item['film_type'] = filme_type

        film_date= bs2_info.find('div', attrs={'class': 'movie-brief-container'}).find_all('li')[-1].text[:10]
        item['film_date'] = film_date
        
        yield item