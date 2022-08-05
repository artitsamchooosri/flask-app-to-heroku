from flask import Flask, jsonify, render_template, request, make_response
from flask_bootstrap import Bootstrap
import os
import uuid
import base64

import json
import numpy as np
import pandas as pd
import requests

from PIL import Image
import warnings

import gspread
from oauth2client.service_account import ServiceAccountCredentials

warnings.simplefilter('error', Image.DecompressionBombWarning)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage, FlexSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__, static_folder='imgs')
bootstrap = Bootstrap(app)

lineaccesstoken = 'gyBAJgxWYGkpKNPDnsuhmW4veeCqOO9kzPv5SGNkhaysTCWXEFwVCtYWGQFstVaaKMGoSoFU/T3PyHrejvHQUzjTQZ/kfKRh06zwfksY9wPlvKPznqom5N0exYWU/aMJU4c9OdMXgbKpczOg6TpTvgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)


####################### new ########################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveimage', methods=['POST'])
def saveimage():
  event = request.form.to_dict()
  print(event['LT'])
  print(event['LO'])
  dir_name = 'imgs'
  img_name = event['LT']+","+event['LO']
  return make_response(img_name, 200)


@app.route('/testpush')
def testpush():
    flex = flexmessage()
    flex = json.loads(flex)
    replyObj = FlexSendMessage(alt_text='Flex Message alt text', contents=flex)
    line_bot_api.push_message('R7f82bdcc51fa937aefe866ab42e68d8c',TextSendMessage(text='https://liff.line.me/1657363028-G2MgkyYb'))
    return '',200

@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200
#fdsd

def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''

    if msgType == "text":
        msg = str(event["message"]["text"])
        replyObj = handle_text(msg)
        line_bot_api.reply_message(rtoken, replyObj)

    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''
def flexmessage():
    flex = '''{"type": "bubble", "size": "giga", "direction": "ltr", "header": {"type": "box", "layout": "vertical", "flex": 0, "spacing": "sm", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "CHECK PICKING", "weight": "bold", "align": "center", "gravity": "center", "contents": []}]}, {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "POOL :", "weight": "bold", "contents": []}, {"type": "text", "text": "MCRR", "color": "#2D870DFF", "contents": []}]}, {"type": "box", "layout": "horizontal", "margin": "md", "contents": [{"type": "text", "text": "Work Order:", "weight": "bold", "contents": []}, {"type": "text", "text": "W2206597", "color": "#2D870DFF", "contents": []}]}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "NAME", "weight": "bold", "contents": []}, {"type": "text", "text": "REAR SPROCKET DAIICHI WAVE100S(428)-35T", "contents": []}]}, {"type": "separator", "margin": "lg", "color": "#0FED10FF"}]}, "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": [{"type": "box", "layout": "vertical", "spacing": "sm", "contents": [{"type": "box", "layout": "baseline", "contents": [{"type": "text", "text": "LINENUM", "weight": "bold", "size": "md", "color": "#000000FF", "gravity": "center", "margin": "none", "decoration": "underline", "contents": []}, {"type": "text", "text": "ITEMBOM", "weight": "bold", "size": "md", "color": "#000000FF", "gravity": "center", "decoration": "underline", "contents": []}, {"type": "text", "text": "\u0e1b\u0e23\u0e30\u0e21\u0e32\u0e13", "weight": "bold", "color": "#000000FF", "gravity": "center", "decoration": "underline", "contents": []}, {"type": "text", "text": "\u0e15\u0e31\u0e14\u0e08\u0e48\u0e32\u0e22\u0e08\u0e23\u0e34\u0e07", "weight": "bold", "color": "#000000FF", "gravity": "center", "decoration": "underline", "contents": []}, {"type": "text", "text": "\u0e2a\u0e48\u0e27\u0e19\u0e15\u0e48\u0e32\u0e07", "weight": "bold", "color": "#000000FF", "gravity": "center", "decoration": "underline", "contents": []}]}, {"type": "box", "layout": "baseline", "contents": [{"type": "text", "text": "1", "contents": []}, {"type": "text", "text": "3B020011", "contents": []}, {"type": "text", "text": "0.553", "contents": []}, {"type": "text", "text": "0.0", "contents": []}, {"type": "text", "text": "0.553", "contents": []}]}, {"type": "box", "layout": "baseline", "contents": [{"type": "text", "text": "2", "contents": []}, {"type": "text", "text": "3A010106", "contents": []}, {"type": "text", "text": "553.000", "contents": []}, {"type": "text", "text": "553.0", "contents": []}, {"type": "text", "text": "0.000", "contents": []}]}, {"type": "box", "layout": "baseline", "contents": [{"type": "text", "text": "3", "contents": []}, {"type": "text", "text": "xxxxxxx", "contents": []}, {"type": "text", "text": "553.000", "contents": []}, {"type": "text", "text": "553.0", "contents": []}, {"type": "text", "text": "0.000", "contents": []}]}]}, {"type": "text", "text": "\u0e15\u0e23\u0e27\u0e08\u0e2a\u0e2d\u0e1a\u0e01\u0e32\u0e23\u0e15\u0e31\u0e14\u0e08\u0e48\u0e32\u0e22\u0e27\u0e31\u0e15\u0e16\u0e38\u0e14\u0e34\u0e1a", "size": "xxs", "color": "#AAAAAA", "wrap": true, "contents": []}]}}'''
    return flex
def handle_text(inpmessage):
    
    if inpmessage == 'ทดสอบ':
        flex = flexmessage()
        flex = json.loads(flex)
        replyObj = FlexSendMessage(alt_text='Flex Message alt text', contents=flex)
    
    else:
        replyObj = FlexSendMessage(text=inpmessage)
    return replyObj

def connect_googlesheet():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    cerds = ServiceAccountCredentials.from_json_keyfile_name("apipython-357807-1e6b7744a8c4.json", scope)
    client = gspread.authorize(cerds)
    return client
if __name__ == '__main__':
    app.run(debug=True)
    google_client=connect_googlesheet()