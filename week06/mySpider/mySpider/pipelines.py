# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from mySpider.ConnMysql import ConnDB

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'ak123',
    'db' : 'test'
}

class MyspiderPipeline:
    # def process_item(self, item, spider):
    #     return item
    def process_item(self, item, spider):
        film_name = item['film_name']
        user_nickname = item['user_nickname']
        short_content = item['short_content']
        film_stars = item['film_stars']

        # output = f'|{film_name}|\t{film_type}|\t{film_date}\n\n'
        # with open(r'.\maoyan_films.txt', 'a+', encoding='utf-8') as file:
        #     file.write(output)
        #     file.close()
          # 一定要返回一个item，否则会抛出异常
        sql = f"insert into movies ( film_name, user_nickname, short_content, film_stars) values('{film_name}','{user_nickname}','{short_content}','{film_stars}');"
        print(sql)
        
        db = ConnDB(dbInfo, sql)
        db.run()
        return item