# -*- coding: utf-8 -*-
import scrapy


class ElectionSpider(scrapy.Spider):
		name = "election"
		start_urls = (
		   'http://eciresults.nic.in/ConstituencywiseS2653.htm?ac=53',

		)

		def parse(self, response):
			state_dict = {'Chhattisgarh' : ['CG'], "Madhya Pradesh" : ["MP"], 'Mizoram' :['MZ'] ,'Rajasthan' : ['RZ'] , 'Telangana' : ['TG']}

			states = response.xpath('//select[@id="ddlState"]//option')
			for state in states[1:]:
				state_name = ''.join(state.xpath('.//text()').extract())
				state_code = ''.join(state.xpath('.//@value').extract())
				#print state_name
				#print state_code
				state_dict[state_name].append(state_code)
				#print state_dict

			const_code = {}
			for value in state_dict.values():
				j, code = value
				constituency = ''.join(response.xpath('//input[@id="Hdn' +j+ '"]//@value').extract()).split(';')
				for i in constituency:
					i = i.split(',')
					if len(i) > 1:
						const_code[i[1]] = i[0]
						url = "http://eciresults.nic.in/Constituencywise" +code +i[0] +".htm?ac="+i[0]	
						yield scrapy.Request(url, callback=self.parse_1, meta={'state_name':state_name , 'constituency_name' : i[1]})


		def parse_1(self,response):
			candidate_details = response.xpath('//div[@id="div1"]//tr')
			candidate_details =  candidate_details[4:-2]
			for details in candidate_details:
				Candidate , Party , Votes = details.xpath('.//text()').extract()
				yield { 'Candidate' : Candidate , 'Party' : Party , 'Votes' : Votes , 'state_name': response.meta['state_name'] , 'constituency_name' : response.meta['constituency_name']}

