# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'faloifyaol'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:9:1600754024:AVdQAGFPWo0hhaQBNT1CNUrW70GANahZx4iltwjsDEkxEbA3wBxyjq7e1Gt4EP3lsGl2py0EPxihxVtAqvJJyIrqV/EVCShDPvtoH+MAt7dNKhe4xnElFrTy2U4gI8ashYjbYj1AQye0gcdK'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['gera_cfirf',
                   'leaf.oliver',
                   'calvin.markham']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'
    foll_hash = [following_hash, followers_hash ]

    def parse(self, response:HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for parse_user in self.parse_users:
                yield response.follow(
                  f'/{parse_user}',
                  self.user_data_parse,
                  cb_kwargs={'username':parse_user}
                    )

    def user_data_parse(self, response:HtmlResponse, username):
        for i in range(0,2):
            follow_hash = self.foll_hash[i]
            user_id = self.fetch_user_id(response.text, username)
            variables={'id':user_id,
                       'first':24}
            url_posts = f'{self.graphql_url}query_hash={follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username':username,
                           'user_id':user_id,
                           'variables':deepcopy(variables),
                           'follow_hash': follow_hash}
            )

    def user_posts_parse(self, response:HtmlResponse,username,user_id,variables, follow_hash):
        j_data = json.loads(response.text)
        if follow_hash == 'c76146de99bb02f6415203be841dd25a':
            gett = 'edge_followed_by'
        else:
            gett = 'edge_follow'
        page_info = j_data.get('data').get('user').get(gett).get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            url_posts = f'{self.graphql_url}query_hash={follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables),
                           'follow_hash': follow_hash}
            )
        if follow_hash == 'c76146de99bb02f6415203be841dd25a':
            status = 'followed'
        else:
            status = 'following'

        follows = j_data.get('data').get('user').get(gett).get('edges')

        for follow in follows:
            item = InstaparserItem(
                user_id = user_id,
                status = status,
                follow_id = follow['node']['id'],
                follow_name = follow['node']['full_name'],
                follow_nick=follow['node']['username'],
                photo = follow['node']['profile_pic_url']
            )
            yield item





    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')