# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import MyspiderItem
import logging

logger = logging.getLogger(__name__)

class ItcastSpider(scrapy.Spider):
	name = 'itcast'
	allowed_domains = ['itcast.cn']
	start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

	def parse(self, response):
		# with open('./teacher.html','w',encoding='utf-8') as f:
		# 	f.write(response.text)
		# items = list()

		for each in response.xpath('//div[@class="li_txt"]'):
			item = MyspiderItem()

			name = each.xpath('h3/text()').extract() # 返回列表
			level = each.xpath('h4/text()').extract()
			info = each.xpath('p/text()').extract()

			item['name'] = name[0]
			item['level'] = level[0]
			item['info'] = info[0]

			#items.append(item)

			yield item

		lesson_list = response.xpath('//div[@class="tea_hd"]/ul/li/@bz').extract()
		for lesson in lesson_list:
			url = 'http://www.itcast.cn/channel/teacher.shtml' + '#' + lesson
			logger.warning(url)
			yield scrapy.Request(url, callback=self.parse)
