# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lm_parser.items import LmParserItem
from scrapy.loader import ItemLoader


class LmRuSpider(scrapy.Spider):
    name = 'lm_ru'
    allowed_domains = ['leroymerlin.ru']
    def __init__(self, search=None):
        super(LmRuSpider, self).__init__()
        self.start_urls = [
            f'https://leroymerlin.ru/search/?q={search}'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()
        if next_page:
            pass
        else:
            next_page = self.allowed_domains[0]
        yield response.follow(next_page, callback=self.parse)

        item_links = response.css(
            'uc-product-list product-card uc-plp-item-new::attr(href)'
        ).extract()

        for item_link in item_links:
            yield response.follow(item_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        loader = ItemLoader(item=LmParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//uc-pdp-price-view/span[1]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('keys', '//dt/text()')
        loader.add_xpath('values', '//dd/text()')
        loader.add_xpath('photo', '//uc-pdp-media-carousel/img/@src')
        yield loader.load_item()