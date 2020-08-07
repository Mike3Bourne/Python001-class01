# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from mySpider.items import MyspiderItem
# from fake_useragent import UserAgent

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    
    def parse(self, response):
        selector = etree.HTML(response.text)
        # movie_info = selector.xpath('//ol[@class="grid_view"]/a')
        film_url = '//ol[@class="grid_view"]/a/@href'
        film_urls = list(selector.xpath(url_path))
        # film_name = '//ol[@class="grid_view"]/a/span[1]/text()'
        # film_name = list(selector.xpath(film_name))
        name_url = zip(film_name, film_urls)
        for name,url in name_url:
            item = MyspiderItem()
            item['film_name'] = name
            url = url + "/reviews"
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse2)
        

    def parse2(self, response):
        item = response.meta['item']
        sel = etree.HTML(response.text)
        user_nickname = list(sel.xpath('//header/a[2]/text()'))
        film_stars = list(sel.xpath('//header/span[1]/@title'))
        short_content = list(sel.xpath('//*[@class="short-content"]/text()[1]'))
        
        # item['film_name'] = film_name
        item['user_nickname'] = user_nickname
        item['film_stars'] = film_stars
        item['short_content'] = short_content
        yield item


