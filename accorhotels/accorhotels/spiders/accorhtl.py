# coding: utf8
import scrapy
import json
from accorhotels.items import AccorhotelsItem

class AccordSpider(scrapy.Spider):
    handle_httpstatus_list = [300]
    name = "accor"
    def start_requests(self):
        url = 'https://secure.accorhotels.com/rest/v2.0/accorhotels.com/hotels?geoCode=PFR&geoType=PA'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_accord = json.loads(response.body)
        for item in json_accord['zone']['child']:
            url = 'https://secure.accorhotels.com/rest'+item['href']
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        json_accord = json.loads(response.body)
        if json_accord['zone']['child']:
            for item in json_accord['zone']['child']:
                url = 'https://secure.accorhotels.com/rest' + item['href']
                yield scrapy.Request(url=url, callback=self.parse1)
        else:
            for item in json_accord['hotel']:
                accord_item = AccorhotelsItem()
                accord_item['name'] = item['name']
                accord_item['address'] = item['address']['country']+', '+item['address']['town']+', '+item['address']['street']
                if item['address']['geoLoc']:
                    accord_item['lat'] = float(item['address']['geoLoc']['latitude'])
                    accord_item['lon'] = float(item['address']['geoLoc']['longitude'])
                else:
                    accord_item['lat'] = 0
                    accord_item['lon'] = 0
                if item['appartHotel']== True:
                    accord_item['category'] = 'appartment'
                else:
                    accord_item['category'] = 'hotel'
                url = 'https://www.accorhotels.com/fr/hotel-'+str(item['code'])+'-'+item['name'].replace(' ','-')+'/index.shtml'
                if item['bookUrl']:
                    accord_item['url'] = item['bookUrl']
                else:
                    accord_item['url'] = ' '
                atrr = []
                for k in item['amenities']:
                    atrr.append(k['label'])
                accord_item['attributes']= ', '.join(atrr)
                yield scrapy.Request(url=url, callback=self.parse2, meta={'accord_item': accord_item})


    def parse2(self, response):
        accord_item = response.meta['accord_item']
        accord_item['link'] = response.url
        accord_item['phone'] = response.xpath(".//meta[@itemprop='telephone']/@content").extract_first(default=' ')
        yield accord_item
