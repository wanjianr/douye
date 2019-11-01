# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    info = scrapy.Field()

class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    list_num = scrapy.Field()
    pic_url = scrapy.Field()
    writer = scrapy.Field()
    price = scrapy.Field()

class AllBookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    book_name = scrapy.Field()
    book_rank = scrapy.Field()
    pic_url = scrapy.Field()
    writer = scrapy.Field()
    price = scrapy.Field()

class DoubanspiderItem(scrapy.Item):
    pic_url = scrapy.Field()
    # ['肖申克的救赎'，'\xa0/\xa0The Shawshank Redamption']
    title = scrapy.Field()
    # content需要处理
    content = scrapy.Field()
    # score = ['9.7','89979人评价']
    score = scrapy.Field()
    info = scrapy.Field()
    intro = scrapy.Field()

class MaoyanspiderItem(scrapy.Item):
    rank = scrapy.Field()
    # ['肖申克的救赎'，'\xa0/\xa0The Shawshank Redamption']
    pic_url = scrapy.Field()
    # content需要处理
    name = scrapy.Field()
    # score = ['9.7','89979人评价']
    actors = scrapy.Field()
    time = scrapy.Field()
    intro = scrapy.Field()
    site = scrapy.Field()
    prize_url = scrapy.Field()
    prize_name = scrapy.Field()
    prize_content = scrapy.Field()