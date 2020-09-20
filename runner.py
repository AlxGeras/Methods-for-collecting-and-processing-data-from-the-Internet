#!/usr/bin/python

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lm_parser import settings
from lm_parser.spiders.lm_ru import LmRuSpider


if __name__ == '__main__':
    search = 'Дом'

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(LmRuSpider, search=search)

    process.start()
