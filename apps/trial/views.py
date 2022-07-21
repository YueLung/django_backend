from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

def hello_world(request):
    return HttpResponse("Hello World!")

def hello_world2(request):
     return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })
    
@api_view(['GET'])
def api_test(request, *args, **kwargs):
    return Response({"data": "api test OK"}, status=200)