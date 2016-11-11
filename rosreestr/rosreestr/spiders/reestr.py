# coding: utf8
import scrapy
import json
import re
from rosreestr.items import RosreestrItem
class AsosSpider(scrapy.Spider):
    name = "reestr"

    def start_requests(self):
        lats = range(471548,473687,2)
        lons = range(394085,398493,2)
        for lat in lats:
            for lon in lons :
                kord = {}
                lonf = float(lon) / 10000
                latf = float(lat) / 10000
                kord['lat'] = latf
                kord['lon'] = lonf
                url = 'http://pkk5.rosreestr.ru/api/features/1?text='+str(latf)+'%20'+str(lonf)+'&tolerance=32&limit=10'
                yield scrapy.Request(url=url, callback=self.parse, meta={'kord': kord})

    def parse(self, response):
        koord = response.meta['kord']
        json_reestr = json.loads(response.body)
        for item in json_reestr['features']:
            adress = RosreestrItem()
            if item['attrs']['address']:
                if re.match(r'61:44',item['attrs']['cn']):
                    adress['address'] = item['attrs']['address']
                    adress['lat'] = koord['lat']
                    adress['lon'] = koord['lon']
                    yield adress

