# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SocietItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
    pass
