#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
class SpidersSpider(scrapy.Spider):
    name = 'medicine'
    #allowed_domains = ['http://www.zysj.com']
    start_urls = [f'http://www.zysj.com.cn/zhongyaocai/index__{page}.html' for page in range(1,24)]

    def parse(self, response):
        details = response.xpath("//div[@id='content']/ul/li/a/@href").extract()
        for i in details:
            details_url = "http://www.zysj.com.cn" + i
            print(details_url)
            yield scrapy.Request(details_url, callback=self.details_parse)

    def details_parse(self, response):

        name = response.xpath("//div[@id='content']/h1/text()")[0].extract()
        pingyint= response.xpath("//div[@id='content']/p[@class='drug py']/text()").extract()
        pingyin = []
        if len(pingyint)>1:
            pingyin = pingyint[1]
        elif len(pingyint)==1:
            pingyin = pingyint[0]
        biemingt = response.xpath("//div[@id='content']/p[@class='drug bm']/text()").extract()
        bieming = []
        if len(biemingt) > 1:
            bieming = biemingt[1]
        elif len(biemingt) == 1:
            bieming = biemingt[0]
        #laiyuan = response.xpath("//div[@id='content']/p[@class='drug ly']/text()").extract()
        laiyuat = response.xpath("//div[@id='content']/p[@class='drug ly']")
        laiyuant = laiyuat.xpath('string(.)').extract()
        laiyuan = []
        if len(laiyuant) > 1:
            laiyuan = laiyuant[1]
        elif len(laiyuant) == 1:
            laiyuan = laiyuant[0]
        xingweit = response.xpath("//div[@id='content']/p[@class='drug xw']/text()").extract()
        xingwei = []
        if len(xingweit) > 1:
            xingwei = xingweit[1]
        elif len(xingweit) == 1:
            xingwei = xingweit[0]
        gongnengt = response.xpath("//div[@id='content']/p[@class='drug gnzz']/text()").extract()
        gongneng = []
        if len(gongnengt) > 1:
            gongneng = gongnengt[1]
        elif len(gongnengt) == 1:
            gongneng = gongnengt[0]
        yongfat = response.xpath("//div[@id='content']/p[@class='drug yfyl']/text()").extract()
        yongfa = []
        if len(yongfat) > 1:
            yongfa = yongfat[1]
        elif len(yongfat) == 1:
            yongfa = yongfat[0]
        zhailuet = response.xpath("//div[@id='content']/p[@class='drug zl']/text()").extract()
        zhailue = []
        if len(zhailuet) > 1:
            zhailue = zhailuet[1]
        elif len(zhailuet) == 1:
            zhailue = zhailuet[0]

        items = {
            'name': name,
            'piny': pingyin,
            'other_name': bieming,
            'laiyuan': laiyuan,
            'xingwei': xingwei,
            'gongneng': gongneng,
            'yongfa': yongfa,
            'zhailu': zhailue,
        }
        yield items