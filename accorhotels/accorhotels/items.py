# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AccorhotelsItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    category = scrapy.Field()
    phone = scrapy.Field()
    link = scrapy.Field()
    url = scrapy.Field()
    attributes = scrapy.Field()


    pass
