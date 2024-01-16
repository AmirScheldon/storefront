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
# we pass a list of strings that specify the HTTP method we support in this endpoint 
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        # here to solve "lots of queries" add "select_related('collection')" to reduce queries.
        queryset = Product.objects.select_related('collection').all()
        # many= True: serializer iterate over the the querset and convert each object to dictionary
        serializer = ProductSerializers(queryset, many= True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        # deserialize data
        serializer = ProductSerializers(data= request.data)
        # we can override validation rules in "serializer.py" with "valid" method
        serializer.is_valid(raise_exception= True)
        # it shows us OrderedDict in our console
        serializer.save()
        return Response('ok')

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk= id)
    # convert our product object to dictonary
    serializer = ProductSerializers(product)
    # serializer.data: gives us the dictionary
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk= pk)
    serializer = CollectionSerializers(collection)
    return Response(serializer.data)
    

