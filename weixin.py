import hashlib
import time
import xml.etree.ElementTree as ET
from config import DevConfig

from flask import Flask, make_response, request

from lyrics import LyricsSearcher

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
        searcher = LyricsSearcher()
        reply = searcher.search_main(content)
        response = make_response(
            xml_rep.format(fromu, tou, int(time.time()), reply))
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
