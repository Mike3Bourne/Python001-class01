# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MyspidersPipeline:
    # def process_item(self, item, spider):
    #     return item

    def process_item(self, item, spider):
        film_name = item['film_name']
        film_type = item['film_type']
        film_date = item['film_date']
        output = f'|{film_name}|\t{film_type}|\t{film_date}\n\n'
        with open(r'.\maoyan_2_films.txt', 'a+', encoding='utf-8') as file:
            file.write(output)
            file.close()
        return item  # 一定要返回一个item，否则会抛出异常
