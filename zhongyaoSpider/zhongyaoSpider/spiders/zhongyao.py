# -*- coding: utf-8 -*-
import scrapy
import logging

from zhongyaoSpider.items import ZhongyaospiderItem


class ZhongyaoSpider(scrapy.Spider):

    name = 'zhongyao'
    allowed_domains = ['zhzyw.com']
    start_urls = ['https://www.zhzyw.com/zycs/zycd/a.html']
    def parse(self, response):

        #first_url="https://www.zhzyw.com/zycs/zycd/a.html"
        next_page =response.xpath("//a[@title='下一页']/@href").extract()
        if next_page:
            for i in next_page:
                next_url="https://www.zhzyw.com"+i
                yield scrapy.Request(next_url,callback=self.parse)
        else:
            next_Letter=response.xpath("//div[@id='piny']/a[position()>=2]/@href").extract()
            for i in next_Letter:
               next_Letter_url = "https://www.zhzyw.com/zycs/zycd/" +i
               yield scrapy.Request(next_Letter_url, callback=self.parse)
        details=response.xpath("//div[@class='ullist01']/ul/li/a/@href").extract()
        for i in details:
            details_url="https://www.zhzyw.com"+i
            yield scrapy.Request(details_url,callback=self.details_parse)
    def details_parse(self,response):
        #dic={}
        content_next_page=response.xpath("//div[@class='pagecontent']/a[@title='下一页']/@href").extract()
        if content_next_page:
            for i in content_next_page:
                content_next_url=response.urljoin(i)
                yield scrapy.Request(content_next_url,callback=self.details_parse)
        logging.debug("使用")
        #from pachong.zhongyaoSpider.zhongyaoSpider.items import ZhongyaospiderItem
        item=ZhongyaospiderItem()
        item['zhongyao_name']=response.xpath("//div[@id='left']/h1/text()").extract()
        item['zhongyao']=response.xpath("//div[@class='webnr']/p/text()").extract()
        #print(item)
        yield item
        # dic['zhongyao']=content
        # yield dic