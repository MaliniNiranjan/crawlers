import requests
import lxml.html
import json

site = requests.get('http://122.15.179.102/tnmarket/home/price_det/')
doc = lxml.html.fromstring(site.content)

crop = doc.xpath('//table//tr')
for i in crop:
	crop_name = ''.join(i.xpath('.//td[3]/text()'))
        crop_variety =''.join(i.xpath('.//td[4]/text()'))
        link = ''.join(i.xpath('.//td[10]/a/@href'))
        #print crop_name
	#print crop_variety
	#print link
	if link:
		site_link = requests.get(link)
		doc1 =  lxml.html.fromstring(site_link.content)

		crop_table= doc1.xpath('//table//tr')
		for i in crop_table:
			comittee = i.xpath('.//td[2]/text()')
        		comittee = ''.join(comittee[1:])
        		RM_name =''.join(i.xpath('.//td[3]/text()'))
			QTY =''.join(i.xpath('.//td[4]/text()'))
			max_price = ''.join(i.xpath('.//td[5]/text()'))
        		min_price = ''.join(i.xpath('.//td[6]/text()'))
        		modal_price = ''.join(i.xpath('.//td[7]/text()'))
        		#print comittee
        		#print RM_name
        		#print QTY
        		#print max_price
        		#print min_price
        		#print modal_price
			data = {'crop_name' : crop_name , 'crop_variety' : crop_variety , 'comittee' : comittee , 'RM_name' : RM_name , 'QTY' : QTY, 'max_price' : max_price , 'min_price' : min_price , 'modal_price' : modal_price}

			print data
			for key,value in data.items():
				with open('agri.json', 'a') as f:
 		        		json.dump("{}: {}".format(key,value), f)    
                        		f.write('\n')

