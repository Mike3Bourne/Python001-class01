

# here put the import lib(scrapy、BeautifulSoup、MyspidersItem)
import scrapy
# from bs4 import BeautifulSoup as bs
from lxml import etree
from mySpiders.items import MyspidersItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan_2'
    allowed_domains = ['maoyan.com']
    
    start_urls = ['https://maoyan.com/films']
      # 从浏览器调试工具中获取相对路径

    def start_requests(self):

        cookies = {'__mta': '19125639.1593093704429.1593275009711.1593355539759.21', 'uuid_n_v': 'v1', 'uuid': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', '_lxsdk_cuid': '172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8', '_lxsdk': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', 'mojo-uuid': 'e1772807c81f11b610e103c16996314e', '_csrf': '9c64c6249d473f7823fba983b17539cee1c9ec205c088dca324030b3ab3ac2ec', 'mojo-session-id': '{"id":"de6b4a539be40e37e53ebb2a95dff803","time":1593355539594}', 'mojo-trace-id': '1', 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1593175457,1593187363,1593223570,1593355540', 'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1593355540', '_lxsdk_s': '172fb6414d0-65c-643-085%7C%7C2'}
        
        url = 'http://maoyan.com/films?showType=3&sortId=1'
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    # def parse(self, response):
    #     pass
    

    def parse(self, response):
        selector = etree.HTML(response.text)
        url_path = '//dd/div[1]/a/@href'  
        film_urls = selector.xpath(url_path)
        maoyan_url = 'https://maoyan.com'
        full_urls = list(map(lambda x: maoyan_url + x, film_urls))
        for film_url in full_urls:
            item = MyspidersItem()
            item['film_url'] = film_url
            yield scrapy.Request(url=film_url, meta={'item':item}, callback=self.parse2)
            if full_urls.index(film_url) > 10:
                break

    def parse2(self, response):
        item = response.meta['item']
        sel = etree.HTML(response.text)
        film_name = ''.join(sel.xpath('//h1[@class="name"]/text()'))
        item['film_name'] = film_name
        film_type = ''.join(sel.xpath('//div[@class="movie-brief-container"]/ul/li[1]/*/text()'))
        item['film_type'] = film_type
        film_date = ''.join(sel.xpath('//div[@class="movie-brief-container"]/ul/li[3]/text()'))[:10]
        item['film_date'] = film_date
        
        yield item