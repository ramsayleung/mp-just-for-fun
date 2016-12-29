#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import xml.etree.ElementTree as ET
from config import DevConfig

from flask import Flask, make_response, request

from lyrics import LyricsSearcher
from translator import Translator

app = Flask(__name__)
app.config.from_object(DevConfig)

xml_rep = "<xml>\
    <ToUserName><![CDATA[{0}]]></ToUserName>\
    <FromUserName><![CDATA[{1}]]></FromUserName>\
    <CreateTime>{2}</CreateTime>\
    <MsgType><![CDATA[text]]></MsgType>\
    <Content><![CDATA[{3}]]></Content>\
    <FuncFlag>0</FuncFlag>\
    </xml>"


@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        token = 'samray'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text.encode('utf-8')
        reply = u'Sam无法识别你的要求哦，要不再检查一下你给Sam的指令'.encode('utf-8')
        if content.startswith('\xe6\xad\x8c\xe8\xaf\x8d'):  #歌词的unicode编码
            content.replace('：', ':')  # 将全角的：转换成半角的:，以防 用户用了全角的:,无法识别
            try:
                key = content.split(':')[1]
            except IndexError, e:  # 原来的unicode编码导致无法用：作分解符split，所以
                #要用unicode分割
                key = content.split('\xef\xbc\x9a')[1]
            searcher = LyricsSearcher()
            reply = searcher.search_main(key)
        elif content.startswith('\xe7\xbf\xbb\xe8\xaf\x91'):  # 翻译的unicode编码
            content.replace('：', ':')  # 将全角的：转换成半角的:，以防 用户用了全角的:,无法识别
            try:
                key = content.split(':')[1]
            except IndexError, e:  # 原来的unicode编码导致无法用：作分解符split，所以
                #要用unicode分割
                key = content.split('\xef\xbc\x9a')[1]
            translator = Translator()
            reply = translator.translator_main(key)
        else:
            pass
        response = make_response(
            xml_rep.format(fromu, tou, int(time.time()), reply))
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
