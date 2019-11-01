# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import BookspiderItem
import logging


logger = logging.getLogger(__name__) # 设置日志运行所在目录为当前目录

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['bang.dangdang.com']
    start_urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2019-7-1-1']

    def parse(self, response):
        for each in response.xpath('//ul/li'):
        	item = BookspiderItem()
        	item['book_name'] = each.xpath('div[3]/a/text()').get()
        	item['list_num'] = each.xpath('div[1]/text()').get()
        	item['price'] = each.xpath('div[7]/p[1]/span[1]/text()').get()
        	item['writer'] = each.xpath('div[5]/a[1]/@title').get()
        	item['pic_url'] = each.xpath('div[2]/a/@href').get()

        	yield item

        total_page = response.xpath('//div[@class="fanye_top"]/div[1]/span[2]/text()').get()
        total_page = int(total_page[1:]) + 1
        for page in range(2,total_page):
        	url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2019-7-1-{}'.format(page)
        	logger.warning(url)
        	yield scrapy.Request(
        		url = url,
        		callback = self.parse
        		)

