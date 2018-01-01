# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    id_name = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    brief = scrapy.Field()
    word_number = scrapy.Field()
    click_count = scrapy.Field()
    hot_share = scrapy.Field()
    update_chapter = scrapy.Field()
    image_add = scrapy.Field()
    pass
class Book_content_Item(scrapy.Item):
    chapter_id = scrapy.Field()
    book_name = scrapy.Field()
    chapter_name= scrapy.Field()
    content = scrapy.Field()
    pass
