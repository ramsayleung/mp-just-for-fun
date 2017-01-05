#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import requests
# from bs4 import BeautifulSoup
from lxml import html
from lxml.html import clean


class LibrarySearcher(object):
    def __init__(self):
        self.url = "http://202.116.174.108:8080/opac/openlink.php?strSearchType=title&historyCount=1&strText=%s&doctype=ALL"
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

        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        return response.content

    def content_parser(self, content):

        data = html.fromstring(content)
        # cleaner = clean.Cleaner(
        #     allow_tags=['table', 'tr', 'td'], remove_unknown_tags=False)
        # cleaner.clean_html(data)
        # self._clean_attrib(data)
        # with open('/tmp/html.html', 'w') as f:
        #     f.write(
        #         html.tostring(
        #             data, encoding='utf-8', pretty_print=True, method='html'))
        #delete "馆藏"
        for i in data.xpath("//ol[@id='search_book_list']/li/p/a"):
            i.getparent().remove(i)
        has_next_page = (
            len(data.xpath("//div[@id='content']/div[5]/span/a")) == 0)
        books_list = map(lambda x: x.text_content(),
                         data.xpath("//ol[@id='search_book_list']/li/h3"))
        books_detail_list = map(
            lambda x: x.text_content().replace(" ", ""),
            data.xpath("//ol[@id='search_book_list']/li/p"))
        # for i in data.xpath("//ol[@id='search_book_list']/li/p/span"):
        #     i.getparent().remove(i)

        # books_publisher_list = map(
        #     lambda x: x.text_content().strip(),
        #     data.xpath("//ol[@id='search_book_list']/li/p"))
        warn = ''
        if not has_next_page:
            warn = u'太多的内容，为了版面整洁，不会一次性全部显示，建议重新输入更详尽的书名\n'.encode('utf-8')
        return warn + "\n\n".join(
            "%s\n%s\n" % tup
            for tup in zip(books_list, books_detail_list)).replace("(0)", "")

    def search_main(self, key):
        url = self.url % key
        return self.content_parser(self.html_downloader(url))

    def _clean_attrib(self, node):
        for n in node:
            self._clean_attrib(n)
        node.attrib.clear()
