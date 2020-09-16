# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient


class JobParserPipeline(object):
    def __init__(self):
        MONGO_URI = 'mongodb://localhost:27017/'
        MONGO_DATABASE = 'vacancy_db'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):

        vacancy_name = ''.join(item['name'])

        salary = item['salary']

        if spider.name == 'hh_ru':

            if salary[0] == 'з/п не указана':
                salary_min = None
                salary_max = None
                salary_currency = None
            else:
                if salary[0] == 'до ':
                    salary_min = None
                    salary_max = int(salary[1].replace('\xa0',''))
                    salary_currency = salary[3]
                elif (salary[0] == 'от ') & (len(salary) < 6):
                    salary_min = int(salary[1].replace('\xa0',''))
                    salary_max = None
                    salary_currency = salary[3]
                else:
                    salary_min = int(salary[1].replace('\xa0',''))
                    salary_max = int(salary[3].replace('\xa0',''))
                    salary_currency = salary[5]

        if spider.name == 'superjob_ru':
            if salary[0] == 'По договорённости':
                salary_min = None
                salary_max = None
                salary_currency = None

            else:
                if salary[0] == 'до':
                    salary = salary[2].split('\xa0')
                    salary_min = None
                    salary_max = int(salary[0] + salary[1])
                    salary_currency = salary[2]
                elif salary[0] == 'от':
                    salary = salary[2].split('\xa0')
                    salary_min = int(salary[0] + salary[1])
                    salary_max = None
                    salary_currency = salary[2]
                elif len(salary) < 4:
                    salary_min = int(salary[0].replace('\xa0', ''))
                    salary_max = None
                    salary_currency = salary[2]
                else:
                    salary_min = int(salary[0].replace('\xa0',''))
                    salary_max = int(salary[4].replace('\xa0',''))
                    salary_currency = salary[6]

        vacancy_link = item['vacancy_link']
        site_scraping = item['site_scraping']

        vacancy_json = {
            'vacancy_name': vacancy_name, \
            'salary_min': salary_min, \
            'salary_max': salary_max, \
            'salary_currency': salary_currency, \
            'vacancy_link': vacancy_link, \
            'site_scraping': site_scraping
        }

        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_json)
        return vacancy_json

    def salary_parse_superjob(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        if salary[0] == 'до':
            salary_max = salary[2]
        elif len(salary) == 3 and salary[0].isdigit():
            salary_max = salary[0]
        elif salary[0] == 'от':
            salary_min = salary[2]
        elif len(salary) > 3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]

        salary_currency = self._get_name_currency(salary[-1])

        result = [
            salary_min, \
            salary_max, \
            salary_currency
        ]
        return result

    def _get_name_currency(self, currency_name):
        currency_dict  = {
            'EUR': {'€'}, \
            'KZT': {'₸'}, \
            'RUB': {'₽', 'руб.'}, \
            'UAH': {'₴', 'грн.'}, \
            'USD': {'$'}
        }

        name = None

        for item_name, items_list in currency_dict.items():
            if currency_name in items_list:
                name = item_name

        return name
