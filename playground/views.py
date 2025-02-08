from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import requests
from rest_framework.views import APIView
from django.utils.decorators import method_decorator

class HelloViewSet(APIView):
    @method_decorator(cache_page(10 * 60))
    def get(self, request):
        response = requests.post('https://httpbin.org/delay/2')
        result = response.json()
        return render(request, 'hello.html', {'name' :'Amir'})       
    
