#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html

import weixin_logger


class LyricsSearcher(object):
    def __init__(self):
        logger = weixin_logger.WeixinLogger(__name__)
        self.logger = logger.get_logger()
        self.search_url = 'http://www.xiami.com/search?key='
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
        # with open('/tmp/fck.html', 'w') as file:
        #     file.write(content)
        return content

    def song_parser(self, content):
        text = html.fromstring(content)
        tag_index = 1
        try:
            song_name = text.xpath(
                "//div[@id='wrapper']/div[2]/div[1]/div/div[2]/div/div[1]/table\
                /tbody[1]/tr/td[2]/a[1]")[0].text
            if song_name is None:
                song_name = text.xpath(
                    "//div[@id='wrapper']/div[2]/div[1]/div/div[2]/div/div[1]\
                    /table/tbody[1]/tr/td[2]/a[2]")[0].text
                tag_index = 2
            else:
                pass
            singer_name = text.xpath(
                "//div[@class='result_main']/table/tbody[1]/tr/td[3]/a")[
                    0].text
            lyrics_url = text.xpath(
                "//div[@class='result_main']/table/tbody[1]/tr/td[2]/a[{}]\
                /@href".format(tag_index))[0]
        except IndexError, e:
            self.logger.warn("找不到该歌词对应的歌曲")
            self.logger.error(e)
            song_name = None
            singer_name = None
            lyrics_url = None
        return song_name, singer_name, lyrics_url

    def lyrics_parser(self, content):
        try:
            text = html.fromstring(content)
            lyrics = text.xpath("//div[@id='lrc']/div[1]")[0].text_content()
        except IndexError, e:
            self.logger.warn("找不到该歌词对应的歌曲")
            self.logger.error(e)
            lyrics = None
        return lyrics

    def search_main(self, key):
        url = self.search_url + key
        content = self.html_downloader(url)
        song_name, singer_name, lyrics_url = self.song_parser(content)
        if song_name is None and singer_name is None:
            reply = u"OMG,你好有品味耶，Sam没办法找到对应的歌曲，要不你再确定一下你的歌词?".encode('utf-8')
        else:
            lyrics = self.lyrics_parser(self.html_downloader(lyrics_url))
            reply = u"艺人:{0} 歌名:{1}\n完整歌词:{2}".format(
                singer_name.strip(), song_name, lyrics).encode('utf-8')
        return reply
