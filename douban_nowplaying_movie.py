#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import os
import pickle

import redis
import requests
from lxml import html


class NowPlayingMovie(object):
    def __init__(self):
        self.redis = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
            password=os.getenv("REDIS_PASSWORD"))
        self.url = 'https://movie.douban.com/nowplaying/guangzhou/'
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
        movie_name_list = []
        movie_rating_list = []
        movie_name_list = data.xpath(
            "//div[@id='nowplaying']/div[2]/ul/li/ul/li[@class='stitle']")
        movie_rating_list = data.xpath(
            "//div[@id='nowplaying']/div[2]/ul/li/ul/li[@class='srating']")
        movie_name_list = map(lambda x: x.text_content().strip(),
                              movie_name_list)
        movie_rating_list = map(
            lambda x: x.text_content().strip().encode('utf-8'),
            movie_rating_list)
        movies = dict(zip(movie_name_list, movie_rating_list))
        sorted_movies = sorted(
            movies.items(), key=lambda x: x[1], reverse=True)
        pickle_obj = pickle.dumps(sorted_movies)
        return pickle_obj

    def movie_store(self, movies):
        # self.redis.hmset("movies", movies)
        self.redis.set('now_playing_movies', movies)

    def movie_main(self):
        self.movie_store(self.movie_parser(self.html_downloader(self.url)))
