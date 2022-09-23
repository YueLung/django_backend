from django.http import HttpResponse

from apps.line.module.crawl import crawl_stock_info


def get_stock_info(request):
    result = crawl_stock_info(['2330', '0050', '00878', '1584'], False)
    return HttpResponse(result)
