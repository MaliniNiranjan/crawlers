# -*- coding: utf-8 -*-
import json
import scrapy


class CardekhoSpider(scrapy.Spider):
    name = "cardekho"
    #allowed_domains = ["https://www.cardekho.com"]
    start_urls = (
        'https://www.cardekho.com/api/v1/usedcar/search?&cityId=105&regionId=0&connectoid=ca55a126-6811-747c-5b6e-bc243583e0fd&sessionid=b5371726235b69aa9a2a09a015e5bd35&searchstring=used-cars%2Bin%2Bbangalore&pagefrom=80&sortby=&sortorder=',
    )

    def parse(self, response):
		json_data = json.loads(response.body)
		json_data = json_data['data']['cars']

		for x in json_data:
			x.pop("vlink")
			x.pop("webp_image")
			x.pop("pi")
			x.pop("position")
			yield x

		if "flag" not in response.meta.keys():
			for page in range(2, 100):
				url = "https://www.cardekho.com/api/v1/usedcar/search?&cityId=105&connectoid=ca55a126-6811-747c-5b6e-bc243583e0fd&sessionid=b5371726235b69aa9a2a09a015e5bd35&regionId=0&searchstring=used-cars%2Bin%2Bbangalore&pagefrom="+ str(page) +"&sortby=&sortorder="
				yield scrapy.Request(url, callback=self.parse, meta={'flag' : True})
