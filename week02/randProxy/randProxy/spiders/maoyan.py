

# here put the import lib(scrapy、BeautifulSoup、randProxyItem)
import scrapy
from lxml import etree
from randProxy.items import RandproxyItem
from fake_useragent import UserAgent

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    
    start_urls = ['https://maoyan.com/films']
      # 从浏览器调试工具中获取相对路径

    def start_requests(self):
        ua = UserAgent(verify_ssl=False)  # FakeUserAgent
        headers = {
            'User-Agent': ua.chrome
        }

        cookies = {'__mta': '19125639.1593093704429.1593935000227.1593951239315.22', 'uuid_n_v': 'v1', 'uuid': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', '_lxsdk_cuid': '172ebc8c872c8-06fb8d7d972ad3-4353760-100200-172ebc8c873c8', '_lxsdk': '66032280B6EC11EA96060F060440817E0CD6588F264341F6BAE592A978223E64', 'mojo-uuid': 'e1772807c81f11b610e103c16996314e', '_csrf': '28431e538fa21f37677725425c76245bb72c74063c1587fd3e779c5afabcaaec', 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1593187363,1593223570,1593355540,1593934899', 'mojo-session-id': '{"id":"4f72b40fffe04a2f9c7e5cef85f6dbba","time":1593951190127}', 'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1593951239', '_lxsdk_s': '1731ee4fc07-e48-b4a-16f%7C%7C5', 'mojo-trace-id': '3'}
        
        url = 'http://maoyan.com/films?showType=3&sortId=1'
        yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    # def parse(self, response):
    #     pass
    

    def parse(self, response):
        selector = etree.HTML(response.text)
        url_path = '//dd/div[1]/a/@href'  
        film_urls = selector.xpath(url_path)
        maoyan_url = 'https://maoyan.com'
        full_urls = list(map(lambda x: maoyan_url + x, film_urls))
        for film_url in full_urls:
            item = RandproxyItem()
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