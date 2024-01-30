from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers, CollectionSerializers, ReviewsSerilizer, CartSerializers, CartItemSerializers, AddCartItemSerializers, UpdateCartItemSerializers
from .models import Product, Collection, OrderItem, Reviews, Cart, CartItem
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
    
class CartVewSets(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializers

class CartItemViewSets(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['carts_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializers
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializers
        return CartItemSerializers
    
    def get_queryset(self):
        return CartItem.objects.\
            filter(cart_id = self.kwargs['carts_pk'])\
            .select_related('product')