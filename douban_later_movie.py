#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle

import redis
import requests
from lxml import html


class LaterPlayingMovie(object):
    def __init__(self):
        self.redis = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
            password=os.getenv("REDIS_PASSWORD"))
        self.url = "https://movie.douban.com/later/guangzhou/"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": "http://www.example.com/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }

    def html_downloader(self, url):
        content = requests.get(url, headers=self.headers).text
        return content

    def movie_parser(self, content):
        data = html.fromstring(content)
        movies_name_list = []
        movies_category_list = []
        movies_area_list = []
        movies_date_list = []
        movies_name_list = data.xpath("//div[@id='showing-soon']/div/div/h3/a")
        movies_date_list = data.xpath(
            "//div[@id='showing-soon']/div/div/ul/li[1]")
        movies_category_list = data.xpath(
            "//div[@id='showing-soon']/div/div/ul/li[2]")
        movies_area_list = data.xpath(
            "//div[@id='showing-soon']/div/div/ul/li[3]")
        movies_name_list = map(lambda x: x.text_content().strip(),
                               movies_name_list)
        movies_date_list = map(lambda x: x.text_content().strip(),
                               movies_date_list)
        movies_category_list = map(lambda x: x.text_content().strip(),
                                   movies_category_list)
        movies_area_list = map(lambda x: x.text_content().strip(),
                               movies_area_list)
        movies = zip(movies_name_list, movies_date_list, movies_category_list,
                     movies_area_list)
        pickle_obj = pickle.dumps(movies)
        return pickle_obj

    def movie_store(self, movies):
        self.redis.set('upcoming_movies', movies)

    def movie_main(self):
        self.movie_store(self.movie_parser(self.html_downloader(self.url)))
