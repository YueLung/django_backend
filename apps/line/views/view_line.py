from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from apps.line.module.crawl import (
    crawl_exchage_rate,
    crawl_stock_info
)


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def bot_reply_message(request):
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
                    response_msg = crawl_stock_info(
                        ['2330', '0050', '00878', '1584'], False)
                elif receive_msg == 'e':
                    response_msg = crawl_exchage_rate()
                else:
                    response_msg = crawl_stock_info(
                        ['2330', '1584', '2345', '2377', '00642U', '00635U'])

                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(response_msg))
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
