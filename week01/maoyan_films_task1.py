
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maoyan_films_task1.py
@Time    :   2020/06/27 11:54:17
@Author  :   Mike
@Contact :   bixshds@163.com
@Department   :  None
@Desc    :   极客大学Python训练营课程1_作业1：
            1. 作业题目：
            安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个电影名称、
            电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
            2. 处理步骤：
            使用requests请求，并获取响应内容
            使用bs4解析网页
            使用pandas 保存电影信息到csv文件中
'''

# here put the import lib(requests、bs4、pandas)
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


maoyan_domain = 'https://maoyan.com'  # 猫眼域名
maoyan_films_url = maoyan_domain + '/films'  # 猫眼电影主页的url

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/83.0.4103.116 Safari/537.36'

# 此cookie是在浏览器中验证通过后获取的，下次再处理这个问题
cookies = '__mta=19125639.1593093704429.1593188514340.1593223589244.17; uuid_n_v=v1; \
    uuid=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; \
    _lxsdk_cuid=172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8; \
    _lxsdk=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; \
    mojo-uuid=e1772807c81f11b610e103c16996314e; \
    _csrf=0fce7216759568c83b3097bf466cb9105aae2480e9248fcdd8c9a1c941c54800; \
    mojo-session-id={"id":"e263f1719b87785cf376a690c1764146","time":1593223569887}; \
    Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593174407,1593175457,1593187363,1593223570; \
    __mta=19125639.1593093704429.1593188514340.1593223570188.17; \
    Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593223589; mojo-trace-id=3; \
    _lxsdk_s=172f386627e-e2a-0ef-325%7C%7C4__mta=19125639.1593093704429.1593223589244.1593223600946.18; \
    uuid_n_v=v1; uuid=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; \
    _lxsdk_cuid=172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8; \
    _lxsdk=66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64; \
    mojo-uuid=e1772807c81f11b610e103c16996314e; \
    _csrf=0fce7216759568c83b3097bf466cb9105aae2480e9248fcdd8c9a1c941c54800; \
    mojo-session-id={"id":"e263f1719b87785cf376a690c1764146","time":1593223569887}; \
    Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593174407,1593175457,1593187363,1593223570; \
    Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593224735; \
    __mta=19125639.1593093704429.1593223600946.1593224735164.19; mojo-trace-id=11; \
    _lxsdk_s=172f386627e-e2a-0ef-325%7C%7C15'

# 定义头信息
header = {}
header['user-agent'] = user_agent
header['cookie'] = cookies

payload = {'showType': 3, 'sortId': 1}

response = requests.get(maoyan_films_url, headers=header, params=payload)

# 使用BeautifulSoup解析这段代码,能够得到一个 BeautifulSoup 的对象:
bs_info = bs(response.text, 'html.parser')


films = []  # 定义存储要获取的所有电影信息的空列表

for stag in bs_info.find_all('span'):

    if type(stag.get('class')) == list:
        # print(stag.get('class'),type(stag.get('class')))

        if stag.get('class')[0] == 'name':
            # print(stag.text)
            film_name = stag.text

        if stag.get('class')[0] == 'hover-tag' and stag.text == '类型:':
            # print('类型：',stag.parent.text.strip().split(' ')[-1])
            film_type = stag.parent.text.strip().split(' ')[-1]

        if stag.get('class')[0] == 'hover-tag' and stag.text == '上映时间:':
            film_datetime = stag.parent.text.strip().split(' ')[-1]
            film = [film_name, film_type, film_datetime]
            films.append(film)
        if len(films) >= 10:
            break

movie = pd.DataFrame(data=films)

movie.to_csv('./maoyan_films_task1.csv',
             encoding='utf-8-sig', index=False, header=False)

