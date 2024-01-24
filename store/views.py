from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers, CollectionSerializers, ReviewsSerilizer
from .models import Product, Collection, OrderItem, Reviews
from .pagination import DefaultPagination
from .filters import ProductFilter

"""
    Django:
        HttpRequest
        HttpResponse
    REST Framework:
        Request
        Response
    which is simpler and more powerful than Django's.

"""
# class base view make us to write cleaner and less code( less if statement)
# it(ModelViewSet) does 'GET', 'POST', 'PUT AND PATCH' and 'DELETE'
# we have ReadOnlyModelViewSet that perform only Get performance
class ProductViewSets(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() > 0:
            return Response({'error': 'product cannot be deleted bcause it include one or more ordered item.'})
        return super().destroy(request, *args, **kwargs)

class CollectionViewSets(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count= Count('products')).all() 
    serializer_class = CollectionSerializers
    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk)
        if collection.products.count() > 0 :
            return Response({'error': 'collection cannot be deleted bcause it include one or more product.'}, status= status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
class ReviewsViewSets(ModelViewSet):
    serializer_class = ReviewsSerilizer

    def get_queryset(self):
        return Reviews.objects.filter(product_id = self.kwargs['products_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['products_pk']}