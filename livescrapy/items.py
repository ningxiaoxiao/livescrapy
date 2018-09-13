# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LivescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform=scrapy.Field()

    roomid=scrapy.Field()#标识
    title=scrapy.Field()
    uid=scrapy.Field()#标识
    username=scrapy.Field()
    fans=scrapy.Field()
    online=scrapy.Field()
    cate=scrapy.Field()
