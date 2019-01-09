# -*- coding: utf-8 -*-
import scrapy
import json

class CricbuzzSpider(scrapy.Spider):
    name = "cricbuzz"
    allowed_domains = ["www.cricbuzz.com"]
    start_urls = (
        'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/3?matchTypes=ALL' ,'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/1?matchTypes=ALL' , 'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/4?matchTypes=ALL', 'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/5?matchTypes=ALL' , 'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/6?matchTypes=ALL','https://cricketapi.platform.iplt20.com/tournaments/10192/squads/8?matchTypes=ALL', 'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/9?matchTypes=ALL' ,'https://cricketapi.platform.iplt20.com/tournaments/10192/squads/62?matchTypes=ALL'    
   )

    def parse(self, response):
	teamdata=response.body
	json1_data = json.loads(teamdata)
	#print type(json1_data)
	#print dir(json)
	#print dir(json1_data)
	#print json1_data["ALL"]['team'].keys()
	
	teamname = json1_data["ALL"]['team']['fullName']
	for i in json1_data["ALL"]['players']: 
		playerid = i['id']
		playername = i['fullName']
		nationality = i['nationality']
		dob = i['dateOfBirth']
		#print i.keys()
		if 'bowlingStyle' in i.keys():
			bowlingstyle = i['bowlingStyle']
		else:
			bowlingstyle = ''
		
		yield{'teamname' : teamname,'playerid' :playerid, 'playername': playername,'nationality' : nationality, 'dob' : dob ,'bowlingstyle' :bowlingstyle}
 
	"""teams=response.xpath('//a[@class="cb-col cb-col-100 cb-font-14"]')
	for k in teams:
		team_name = ''.join(k.xpath('.//div[@class="cb-col cb-col-80"]/div[@class="cb-font-18"]/text()').extract())
		start_price = k.xpath('.//div[@class="cb-col cb-col-33 cb-lst-itm-sm"]/div[@class="cb-font-18"]/text()').extract()
		purse_to_start = start_price[0]
		purse_remaining = start_price[1]
		squad_size = start_price[2]
		link=k.xpath('.//@href').extract()
		team_link = "https://www.cricbuzz.com"+ link[0] 	
		print purse_to_start
		print purse_remaining
		print squad_size
		print team_link
		yield scrapy.Request(team_link, self.parse_page1, meta={'team_name' : team_name, 'purse_to_start' : purse_to_start, 'squad_size' : squad_size, 'purse_remaining' : purse_remaining}) """

    def parse_page1(self,response):
	team_details=response.xpath('//div[@class="cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm cb-schdl"]')
	for i in team_details:
		player_name = ''.join(i.xpath('.//div[@class="cb-col cb-col-80"]/div[@class="cb-font-18"]/text()').extract())
		price = i.xpath('.//div[contains(@class, "cb-col cb-col-20 cb-lst-itm-sm text-right")]//text()').extract()
		base_price = price[0]
		final_price = price[1]
		cnt_pos = ''.join(i.xpath('.//div[@class="cb-font-12 text-gray"]//text()').extract())
		position, country = '', ''
		if "\xe2\x80\xa2" in cnt_pos.encode('utf-8'):
			position, country = cnt_pos.encode('utf-8').split("\xe2\x80\xa2")

		print "*"*40
		print player_name.strip()
		print base_price
		print final_price
		print country.strip()
		print position.strip()
		print '\n' 
