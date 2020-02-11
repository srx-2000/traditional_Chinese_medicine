# -*- coding: utf-8 -*-
import scrapy


class Zhongyiyao4Spider(scrapy.Spider):
    name = 'zhongyiyao4'
    allowed_domains = ['zhongcaoyao.51240.com']
    start_urls = [f'https://zhongcaoyao.51240.com/pwshj_{page}__zhongcaoyaolist/'for page in range(1,21)]

    def parse(self, response):
        zhongyao_list=response.xpath("//ul[@class='list']/li/a/@href").
