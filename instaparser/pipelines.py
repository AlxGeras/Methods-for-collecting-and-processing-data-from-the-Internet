# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        MONGO_URI = 'mongodb://localhost:27017/'
        MONGO_DATABASE = 'insta'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):

        user_id = item['user_id']

        status = item['status']

        follow_id = item['follow_id']

        follow_name = item['follow_name']

        follow_nick = item['follow_nick']


        photo = item['photo']


        insta_json = {
            'user_id': user_id, \
            'status': status, \
            'follow_id': follow_id, \
            'follow_name': follow_name, \
            'follow_nick': follow_nick, \
            'photo' : photo

        }

        collection = self.mongo_base[spider.name]
        collection.insert_one(insta_json)
        return insta_json