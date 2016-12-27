import hashlib
import xml.etree.ElementTree as ET
from config import DevConfig

from flask import Flask, make_response, request

app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/weixin/index')
def index():
    return "Index,successful"


@app.route('/weixin')
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
            content = xml_rec.find('Content').text
            xml_rep = "<xml>\
                <ToUserName><![CDATA[%s]]></ToUserName>\
                <FromUserName><![CDATA[%s]]></FromUserName>\
                <CreateTime>%s</CreateTime>\
                <MsgType><![CDATA[text]]></MsgType>\
                <Content><![CDATA[%s]]></Content>\
                <FuncFlag>0</FuncFlag>\
                </xml>"

    # return "helloworld"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
