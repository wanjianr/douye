# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider

import scrapy
from copy import deepcopy
from mySpider.items import MaoyanspiderItem
import logging


logger = logging.getLogger(__name__)

class MaoyanSpider(CrawlSpider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # https://maoyan.com/board/4?offset=0
    start = 0
    url = 'https://maoyan.com/board/4?offset='
    start_urls = [url + str(start)]

    def parse(self, response):
        item = MaoyanspiderItem()

        movies = response.xpath("//*[@id='app']/div/div/div[1]/dl/dd")
        logger.warning('--响应成功--')
        for each in movies:
            logger.warning('--正在抓取列表页面信息--')
            item['rank'] = int(each.xpath("i/text()").extract_first())
            item['pic_url'] = each.xpath('a/img[2]/@data-src').extract_first()
            item['name'] = each.xpath('div/div/div[1]/p[1]/a/text()').extract_first()
            item['actors'] = each.xpath('div/div/div[1]/p[2]/text()').extract_first().strip()
            item['time'] = each.xpath('div/div/div[1]/p[3]/text()').extract_first()
            url = 'https://maoyan.com' + each.xpath('div/div/div[1]/p[1]/a/@href').extract_first()
            logger.warning(url)
            yield scrapy.Request(
                url,
                callback = self.detail_page,
                meta = {'item':deepcopy(item)}
                )

        if self.start <= 100:
            self.start += 10
            yield scrapy.Request(self.url + str(self.start), callback=self.parse)

    def detail_page(self, response):
        logger.warning('--正在抓取详情页面信息--')
        item = response.meta['item'] 
        item['intro'] = response.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/span/text()').extract_first()
        item['site'] = response.xpath('//*/div[3]/div/div[2]/div[1]/ul/li[2]/text()').extract_first().strip()
        prize = response.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[3]/div[2]/ul/li')
        prize_url = []
        prize_name = []
        prize_content = []
        for each in prize:
            prize_url.append(each.xpath('div[1]/div/img/@src').extract_first())
            prize_name.append(each.xpath('div[1]/text()').extract()[1].strip())
            prize_content.append(each.xpath('div[2]/div/text()').extract_first())
        item['prize_url'] = str(prize_url)
        item['prize_name'] = str(prize_name)
        item['prize_content'] = str(prize_content)
        yield item
