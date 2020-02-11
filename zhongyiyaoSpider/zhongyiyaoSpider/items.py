# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongyiyaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    piny= scrapy.Field()
    laiyuan=scrapy.Field()
    other_name=scrapy.Field()
    xingwei=scrapy.Field()
    gongneng=scrapy.Field()
    yongfa=scrapy.Field()
    zhailu=scrapy.Field()
