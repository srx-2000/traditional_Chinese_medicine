# -*- coding: utf-8 -*-
import scrapy

import logging
import re
from ..items import ZhongyiyaospiderItem


class ZhongyiyaoSpider(scrapy.Spider):
    name = 'zhongyiyao'
    allowed_domains = ['zhongyaocai360.com']
    start_urls = ['http://zhongyaocai360.com/zhongyaodacidian/']

    def parse(self, response):
        zhongyao_list=response.xpath("//div[@class='spider']/ul/li/a/@href").extract()
        if zhongyao_list:
            for i in  zhongyao_list:
                detail_urls=response.urljoin(i)
                yield scrapy.Request(detail_urls,callback=self.detail_parse)
    def detail_parse(self,response):
        name=[]
        name=response.xpath("//h2/text()").re("《.*")[0]
        gongneng=[]
        zhongyao_zhuzhi_url=response.xpath("//div[@class='gnzzp']/p")
        for i in zhongyao_zhuzhi_url:
            gongneng=i.xpath("string(.)")[0].extract()
        piny=[]
        other_name=[]
        laiyuan=[]
        xingwei=[]
        yongfa=[]
        zhailu=[]

        zhongyao_content=response.xpath("//p")
        if zhongyao_content:
            for i in zhongyao_content:
                content=i.xpath("string(.)")
                if content.re("【拼音.*"):
                    piny=content[0].extract()
                if content.re("【别名.*"):
                    other_name=content[0].extract()
                if content.re("【来源.*"):
                    laiyuan=content[0].extract()
                if content.re("【性味.*"):
                    xingwei=content[0].extract()
                if content.re("【用法.*"):
                    yongfa=content[0].extract()
                if content.re("【摘录.*"):
                    zhailu=content[0].extract()
        item={
            "name":name,
            "gongneng":gongneng,
            'other_name':other_name,
            "yongfa":yongfa,
            "xingwei":xingwei,
            "zhailu":zhailu,
            "laiyuan":laiyuan,
            "piny":piny
        }
        yield item
        #zhongyao_content=response.xpath("").extract()
