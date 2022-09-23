from django.contrib import admin
from django.urls import path

from .views import (
    view_line,
    view_stock,
    view_exchange_rate
)

urlpatterns = [
    path('', view_line.bot_reply_message),
    path('crawl-test/stock', view_stock.get_stock_info),
    path('crawl-test/exchage-rate', view_exchange_rate.get_exchage_rate),
]
