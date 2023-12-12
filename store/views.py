from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

"""
    Django:
        HttpRequest
        HttpResponse
    REST Framework:
        Request
        Response
    which is simpler and more powerful than Django's.
    
"""

# this func gives use "The browseable api" which make incredibly easy to test our api EndPoint in browser.
@api_view()
def product_list(request):
    return Response('ok')

@api_view()
def product_detail(request, id):
    return Response(id)

