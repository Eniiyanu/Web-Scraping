# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ClimateBase(scrapy.Item):
    job_title = scrapy.Field()
    company = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    date_posted = scrapy.Field()

class Unicef(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()

class Glassdoor(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
