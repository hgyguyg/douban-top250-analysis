# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    date = scrapy.Field()
    rating_num = scrapy.Field()
    rating_people = scrapy.Field()
    director = scrapy.Field()
    attrs = scrapy.Field()
    rank = scrapy.Field()


