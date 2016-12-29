#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from weixin_logger import WeixinLogger


class Translator(object):
    def __init__(self):
        logger = WeixinLogger(__name__)
        self.youdao_url = 'http://fanyi.youdao.com/openapi.do?keyfrom=SamrayJustForFun&key=1532877421&type=data&doctype=json&version=1.1&q='
        self.logger = logger.get_logger()
        self.key = ''

    def url_request(self, url):
        data = requests.get(url).json()
        return data

    def data_parse(self, data):
        # 翻译单词
        try:
            if data["errorCode"] == 0:
                translation = data["translation"]
                us_phonetic = data["basic"]["us-phonetic"]
                phonetic = data["basic"]["phonetic"]
                uk_phonetic = data["basic"]["phonetic"]
                explains = []
                detailed_explains = ''.join(data["basic"]["explains"])
                reply = u"{0}:\\n翻译:{1}\\n 美式发音:{2}\\n 英式发音:{3}\\n词义解释:{4}".format(
                    self.key, translation, us_phonetic, uk_phonetic,
                    detailed_explains).encode('utf-8')
            elif data["errorCode"] == 20:
                reply = u"哎呀，要Sam翻译的文本过长啦".encode('utf-8')
                self.logger.warn(reply)
            elif data["errorCode"] == 30:
                reply = u"哎呀，Sam无法进行有效的翻译啦".encode('utf-8')
                self.logger.warn(reply)
            elif data["errorCode"] == 40:
                reply = u"哎呀，这是Sam不支持的语言类型啦"
                self.logger.warn(reply)
            else:
                reply = u"哎呀，你输入的单词{}Sam看不懂啦，要不你再检查\
                检查".format(self.key).encode('utf-8')
                self.logger.warn(reply)
        except KeyError, e:
            try:
                translation = data["web"][0]["value"]
                reply = u"{0}:\\n 翻译:{1}\\n".format(
                    self.key, translation).encode('utf-8')
            except KeyError, e:
                self.logger.warn("无法找到正确的翻译")
                self.logger.error(e)
                reply = u"哎呀，Sam无法进行有效的翻译啦，要不你再检查一下单词拼写".encode('utf-8')

        return reply

    def translator_main(self, key):
        self.key = key
        url = self.youdao_url + key
        return self.data_parse(self.url_request(url))
