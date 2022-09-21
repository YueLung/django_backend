from cmath import log
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import requests
from bs4 import BeautifulSoup

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

        stockInfos = get_stock_infos()

        for event in events:
            if isinstance(event, MessageEvent):
                stockInfos = 'error'
                receive_msg = event.message.text
                stockInfos = get_stock_infos(
                    ['2330', '0050', '00878', '1584'])
                # if receive_msg in {'qq', 'QQ'}:
                #     stockInfos = get_stock_infos(
                #         ['2330', '0050', '00878', '1584'])
                # else:
                #     stockInfos = get_stock_infos(['2330', '1584'])

                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(stockInfos))
        return HttpResponse()

    else:
        return HttpResponseBadRequest()


# https://www.learncodewithmike.com/2020/02/python-beautifulsoup-web-scraper.html
def get_stock_infos(stockCodes):
    result = []

    for code in stockCodes:
        response = requests.get(f'https://invest.cnyes.com/twstock/TWS/{code}')
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.select_one('.info-lp').getText()
        changePrice = soup.select_one('.change-net').getText()
        changepercent = soup.select_one('.change-percent').getText()
        result.append(f'{code}: {price}  {changePrice}  {changepercent}')

    return ',\n'.join(result)


def crawlTest(request):
    result = get_stock_infos(['2330', '0050', '00878', '1584'])
    return HttpResponse(result)
