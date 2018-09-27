# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    uid = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    rat = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    actors = scrapy.Field()
    types = scrapy.Field()
    tags = scrapy.Field()
