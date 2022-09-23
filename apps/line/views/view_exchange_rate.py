from django.http import HttpResponse
from apps.line.module.crawl import crawl_exchage_rate


def get_exchage_rate(request):
    result = crawl_exchage_rate()
    return HttpResponse(result)
