# -*- coding: utf-8 -*-
import scrapy


class Iplt20Spider(scrapy.Spider):
    name = "iplt20"
    start_urls = (
        'https://www.iplt20.com/teams',
    )

    def parse(self, response):
        ipllinks=response.xpath('//div[@class="col-12"]//li[@class="team-card-grid__item"]/a')
	for i in ipllinks:
		links=i.xpath('.//@href').extract()
		team_links = "https://www.iplt20.com" + links[0]
		yield scrapy.Request(team_links,self.parse_page1)	


    def parse_page1(self,response):
	squad_link=response.xpath('//ul[@class="playersList js-players"]/li/a')
	print squad_link
	for i in squad_link:
		player_link=i.xpath('.//@href').extract()
		players = "https://www.iplt20.com" + player_link[0]
		print players  
		
