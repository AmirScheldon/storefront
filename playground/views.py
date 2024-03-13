from django.db import transaction
from django.shortcuts import render
from store.models import Order, OrderItem
from .tasks import notify_customers


def hello(request):
    notify_customers.delay('hello')
    return render(request, 'hello.html', {'name' :"Amir"})
