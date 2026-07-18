# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    Title = scrapy.Field()
    Rating = scrapy.Field()
    Description = scrapy.Field()
    Availability = scrapy.Field()
    Price = scrapy.Field()
    Url = scrapy.Field()