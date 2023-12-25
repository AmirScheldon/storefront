from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializers, CollectionSerializers

"""
    Django:
        HttpRequest
        HttpResponse
    REST Framework:
        Request
        Response
    which is simpler and more powerful than Django's.
    
"""
# 2.String(store/serializers/ProductSerializers)
# this func gives use "The browseable api" which make incredibly easy to test our api EndPoint in browser.
@api_view()
def product_list(request):
    # here to solve "lots of queries" add "select_related('collection')" to reduce queries.
    queryset = Product.objects.select_related('collection').all()
    # many= True: serializer iterate over the the querset and convert each object to dictionary
    serializer = ProductSerializers(queryset, many= True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk= id)
    # convert our product object to dictonary
    serializer = ProductSerializers(product)
    # serializer.data: gives us the dictionary
    return Response(serializer.data)

# @api_view()
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection, pk= pk)
#     serializer = CollectionSerializers(collection)
#     return Response(serializer.data)
    

