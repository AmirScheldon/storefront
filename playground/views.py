from django.db import transaction
from django.shortcuts import render
from store.models import Order, OrderItem


def hello(request):
    #...
    
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()
        
        order_item = OrderItem()
        order_item.order = order
        order_item.product_id = 1
        order_item.quantity = 1
        order_item.unit_price = 20
        order_item.save()
    
    
    return render(request, 'hello.html', {'name' :"Amir"})
