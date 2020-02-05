# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongyaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    zhongyao_name=scrapy.Field()
    zhongyao = scrapy.Field()

