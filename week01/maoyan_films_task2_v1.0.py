#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maoyan_films_task2_v1.0.py
@Time    :   2020/06/27 11:58:54
@Author  :   Mike
@Contact :   bixshds@163.com
@Department   : None 
@Desc    :   极客大学Python训练营课程1_作业2_v1.0：
            1. 作业题目：
            使用 Scrapy 框架和 XPath 抓取猫眼电影的前 10 个电影名称、电影类型和上映时间，
            并以 UTF-8 字符集保存到 csv 格式的文件中。
            2. 处理步骤：
            此为v1.0版本：忘记用Scrapy框架了
'''

# here put the import lib(requests、lxml、pandas、time)
import requests
from lxml import etree
import pandas as pd
from time import sleep
# import csv

maoyan_domain = 'https://maoyan.com'
maoyan_films_url = maoyan_domain + '/films'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
cookies = '__mta=19125639.1593093704429.1593188514340.1593223589244.17; uuid_n_v=v1; uuid=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; _lxsdk_cuid=172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8; _lxsdk=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; mojo-uuid=e1772807c81f11b610e103c16996314e; _csrf=0fce7216759568c83b3097bf466cb9105aae2480e9248fcdd8c9a1c941c54800; mojo-session-id={"id":"e263f1719b87785cf376a690c1764146","time":1593223569887}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593174407,1593175457,1593187363,1593223570; __mta=19125639.1593093704429.1593188514340.1593223570188.17; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593223589; mojo-trace-id=3; _lxsdk_s=172f386627e-e2a-0ef-325%7C%7C4__mta=19125639.1593093704429.1593223589244.1593223600946.18; uuid_n_v=v1; uuid=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; _lxsdk_cuid=172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8; _lxsdk=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; mojo-uuid=e1772807c81f11b610e103c16996314e; _csrf=0fce7216759568c83b3097bf466cb9105aae2480e9248fcdd8c9a1c941c54800; mojo-session-id={"id":"e263f1719b87785cf376a690c1764146","time":1593223569887}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593174407,1593175457,1593187363,1593223570; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593224735; __mta=19125639.1593093704429.1593223600946.1593224735164.19; mojo-trace-id=11; _lxsdk_s=172f386627e-e2a-0ef-325%7C%7C15'

header = {}
header['user-agent'] = user_agent
header['cookie'] = cookies

payload = {'showType': 3, 'sortId': 1}

# 获取猫眼电影列表页面的响应内容并解析
response = requests.get(maoyan_films_url, headers=header, params=payload)
selector = etree.HTML(response.text)
# 获取猫眼电影列表页面的所有电影详情页面连接

url_path = '//dd/div[1]/a/@href'  # 从浏览器调试工具中获取相对路径
# 获取url
film_urls = selector.xpath(url_path)
full_urls = list(map(lambda x: maoyan_domain + x, film_urls))

# 从每个电影详情页面提取需要的信息


def get_detail_info(sel):
    film_name = ''.join(sel.xpath('//h1[@class="name"]/text()'))
    film_type = ''.join(sel.xpath('//div[@class="movie-brief-container"]/ul/li[1]/*/text()'))
    film_date = ''.join(sel.xpath('//div[@class="movie-brief-container"]/ul/li[3]/text()'))[:10]
    film = [film_name, film_type, film_date]
    return film


# 获取当前页面的所有电影链接
film_info = []
for ful_url in full_urls[:9]:
    # 请求每个电影对应的详情页面，并进行xml处理
    res = requests.get(ful_url, headers=header, params=payload)
    selector_detail = etree.HTML(res.text)
    detail_info = get_detail_info(selector_detail)
    film_info.append(detail_info)
    sleep(1)
print(film_info)

movie = pd.DataFrame(data=film_info)

movie.to_csv('./maoyan_films_task2_v1.0.csv',
             encoding='utf-8-sig', index=False, header=False)

# csv_header = ['电影名','类型','上映时间']
# with open('maoyan_films_info.csv','w',encoding='utf8', newline='') as t:
#     writer = csv.writer(t)
#     writer.writerow(csv_header)
#     writer.writerows(films)
