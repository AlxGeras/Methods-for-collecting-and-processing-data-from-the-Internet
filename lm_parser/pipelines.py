# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
import os
from urllib.parse import urlparse
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class ItemParserPipeline(object):
    def __init__(self):
        MONGO_URI = 'mongodb://localhost:27017/'
        MONGO_DATABASE = 'lm_db'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):
        item_name = ''.join(item['name'])

        item_price = item['price']

        item_link = item['link']
        item_photo = item['photo']

        item_keys = item['keys']

        item_values = item['values']

        item_params = {}

        for key, value in zip(item_keys, item_values):
            item_params[key] = value

        collection = self.mongo_base[spider.name]

        i = 1
        first_name = item_name

        while True:
            if collection.find_one({'item_name': item_name}):
                item_name = f'{first_name}_{i}'
                i += 1
            else:
                break

        item_json = {
            'item_name': item_name, \
            'item_price': item_price, \
            'item_link': item_link, \
            'item_params': item_params, \
            'photo': item_photo
        }

        collection.insert_one(item_json)
        return item_json


class ItemPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    img = img.replace('w_82,h_82', 'w_1000,h_1000')
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        MONGO_URI = 'mongodb://localhost:27017/'
        MONGO_DATABASE = 'lm_db'

        client = MongoClient(MONGO_URI)
        mongo_base = client[MONGO_DATABASE]
        url = request.url
        url = url.replace('w_1000,h_1000', 'w_82,h_82')
        collection = mongo_base[info.spider.name]
        c = collection.find_one({'photo': url})
        path = c['item_name']
        return path + '/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]

            item_name = ''.join(item['item_name'])

            item_price = item['item_price']

            item_link = item['item_link']

            item_params = item['item_params']

            item_photo = item['photo']

            item_json = {
                'item_name': item_name, \
                'item_price': item_price, \
                'item_link': item_link, \
                'item_params': item_params, \
                'photo': item_photo
            }

        MONGO_URI = 'mongodb://localhost:27017/'
        MONGO_DATABASE = 'lm_db'

        client = MongoClient(MONGO_URI)
        mongo_base = client[MONGO_DATABASE]
        collection = mongo_base[info.spider.name]
        collection.update({"item_name": item_name}, {"$set": {"photo": item_photo}})

        return item_json