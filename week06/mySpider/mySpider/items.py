# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MyspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class MyspiderItem(scrapy.Item):
    film_name = scrapy.Field()
    user_nickname = scrapy.Field()
    short_content = scrapy.Field()
    film_stars = scrapy.Field()
    

