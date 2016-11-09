# coding: utf8
import scrapy
import json
from rosreestr.items import RosreestrItem
class AsosSpider(scrapy.Spider):
    name = "reestr"

    def start_requests(self):
        url = 'http://pkk5.rosreestr.ru/api/features/1?text=%D0%92%20%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%D1%85%20%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0%2061:44&tolerance=512&limit=100000&sqo=61:44&sqot=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print response.body
        adress = RosreestrItem()
        json_reestr = json.loads(response.body)
        for item in json_reestr['features']:
            if item['attrs']['address']:
                str = item['attrs']['address']
                adress['address'] = str.encode('utf-8')
                adress['lat'] = item['center']['x']
                adress['lon'] = item['center']['y']
                yield adress
