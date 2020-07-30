# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    phonetic = scrapy.Field()
    other_name = scrapy.Field()
    origine = scrapy.Field()
    taste = scrapy.Field()
    function = scrapy.Field()
    usage = scrapy.Field()
    extract = scrapy.Field()
