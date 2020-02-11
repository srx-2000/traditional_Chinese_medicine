# -*- coding: utf-8 -*-
import scrapy


class Zhongyiyao4Spider(scrapy.Spider):
    name = 'zhongyiyao3'
    allowed_domains = ['daquan.com']
    start_urls = [f'https://www.daquan.com/cyzy/zy{page}.html' for page in range(1,6022)]

    def parse(self, response):
        name = []
        piny = []
        other_name = []
        laiyuan = []
        xingwei = []
        yongfa = []
        zhailu = []
        gongneng = []
        name = response.xpath("//h1/text()")[0].extract()
        content = response.xpath("//div[@class='content']/p[br]")
        content_string=content.xpath("./text()")
        if content_string:
            for i in content_string:
                if i.re("【来源.*"):
                    laiyuan = i.extract().strip()
                if i.re("【用法.*"):
                    yongfa = i.extract().strip()
                if i.re("【功用.*"):
                    gongneng = i.extract().strip()
                if i.re("【拼音.*"):
                    piny = i.extract().strip()
                if i.re("【异名.*"):
                    other_name = i.extract().strip()
                if i.re("【性味.*"):
                    xingwei = i.extract().strip()
                if i.re("^\s+\(《[\u4e00-\u9fa5]+》\)$"):
                    zhailu = i.extract().strip()
        item = {
            "name": name,
            "gongneng": gongneng,
            'other_name': other_name,
            "yongfa": yongfa,
            "xingwei": xingwei,
            "zhailu": zhailu,
            "laiyuan": laiyuan,
            "piny": piny
        }
        # print(item)
        yield item
