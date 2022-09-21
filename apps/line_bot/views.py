from cmath import log
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import requests
from bs4 import BeautifulSoup

import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                receive_msg = event.message.text
                response_msg = None

                if receive_msg in {'q', 'Q'}:
                    response_msg = get_stock_infos(
                        ['2330', '0050', '00878', '1584'], False)
                elif receive_msg == 'e':
                    response_msg = get_exchage_rate()
                else:
                    response_msg = get_stock_infos(
                        ['2330', '1584', '2345', '2377', '00642U', '00635U'])

                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(response_msg))
        return HttpResponse()

    else:
        return HttpResponseBadRequest()


# https://www.learncodewithmike.com/2020/02/python-beautifulsoup-web-scraper.html
def get_stock_infos(stockCodes, isAddName=True):
    result = []

    for code in stockCodes:
        response = requests.get(f'https://invest.cnyes.com/twstock/TWS/{code}')
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.select_one('.info-lp').getText()
        changePrice = soup.select_one('.change-net').getText()
        changepercent = soup.select_one('.change-percent').getText()
        name = soup.select_one('.header_second').getText()
        if isAddName:
            result.append(
                f'{code} {name}: {price}  {changePrice}  {changepercent}')
        else:
            result.append(
                f'{code}: {price}  {changePrice}  {changepercent}')

    return ',\n'.join(result)


def get_exchage_rate():
    now = datetime.datetime.now()
    year = str(now.year)
    month = '{:02d}'.format(now.month)

    response = requests.post(
        f'https://portal.sw.nat.gov.tw/APGQO/GC331!query?formBean.year={year}&formBean.mon={month}').json()

    cny_list = [x for x in response['data'] if x['CRRN_CD'] == 'CNY']

    result = []
    for info in cny_list:
        day = None
        if info['TEN_DAY'] == '1':
            day = '1-10'
        elif info['TEN_DAY'] == '2':
            day = '11-20'
        elif info['TEN_DAY'] == '3':
            day = '21-31'

        result.append(
            f"{info['CRRN_CD']} {info['YEAR']}/{info['MON']} {day}=> {info['IN_RATE']}")

    return ',\n'.join(result)


def crawl_stock(request):
    result = get_stock_infos(['2330', '0050', '00878', '1584'], False)
    return HttpResponse(result)


def crawl_exchage_rate(request):
    result = get_exchage_rate()
    return HttpResponse(result)
