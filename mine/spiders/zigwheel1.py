# -*- coding: utf-8 -*-
import scrapy


class Zigwheel1Spider(scrapy.Spider):
    name = "zigwheel1"
    allowed_domains = ["www.zigwheels.com"]
    start_urls = ['https://www.zigwheels.com/newcars/']

    def parse(self, response):
	brands=response.xpath('//li[@class="gscr_lslide"]/a')
	for i in brands:
		brand_links=i.xpath('.//@href').extract_first()
		print brand_links
