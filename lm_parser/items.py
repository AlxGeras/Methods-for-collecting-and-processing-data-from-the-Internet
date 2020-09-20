# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import MapCompose, TakeFirst


def price_to_int(price):
    if price:
        price = price.replace(' ', '')
        return int(price)
    return price


def remove_gap(value):
    value = value.replace('\n', '').replace(' ', '')
    return value


def remove_dot(key):
    key = key.replace('.', '')
    return key


class LmParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_int),output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    keys = scrapy.Field(input_processor=MapCompose(remove_dot))
    values = scrapy.Field(input_processor=MapCompose(remove_gap))
    photo = scrapy.Field()