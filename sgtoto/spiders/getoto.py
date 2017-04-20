# -*- coding: utf-8 -*-
import scrapy

from scrapy import Spider
from scrapy.selector import Selector

from sgtoto.items import SgtotoItem

class GetotoSpider(scrapy.Spider):
    name = "getoto"
    allowed_domains = ["http://www.asiaone.com/lottery/toto"]
    start_urls = ['http://www.asiaone.com/lottery/toto']

    def parse(self, response):
        #Definining the StackItem
        item = SgtotoItem()

        #extracting the draw date
        item['drawdate'] =  response.xpath('//*[@class="date-display-single"]/text()').extract_first()

	#extracting the draw serial no.
        draw_serial = response.xpath('//*[@class="result-show"]/h3/span[2]/text()').re(r'Draw No. (\w+)')
        item['latestdraw'] = draw_serial[0]
	
	#extracting the winning numbers
        count = 0
        winning_numbers = []
        for numbers in response.xpath('//*[@class="toto-lottery"]/div[1]/div[3]/span/text()').extract():
            if count == 6:
                break
            else:
                winning_numbers.append(numbers)
                count += 1
        item['winning_numbers_field'] = winning_numbers

        yield item
