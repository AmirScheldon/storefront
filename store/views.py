from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import ProductSerializers, CollectionSerializers, ReviewsSerilizer,\
                         CartSerializers, CartItemSerializers, AddCartItemSerializers,\
                         UpdateCartItemSerializers, CustomerSerializers, OrderSerializers,\
                         CreateOrderSerializers, UpdateOrderSerializers, ProductImageSerializers
from .models import Product, Collection, OrderItem, ProductImage, Reviews, Cart, CartItem, Customer, Order
from .pagination import DefaultPagination
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, CustomeDjangoModelPermissions, ViewCustomerHistoryPermission

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
    queryset = Product.objects.prefetch_related('image').all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
    
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
            

class CustomerViewSets(ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [IsAdminUser]
    
    @action(detail= True, permission_classes= [ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

#to add any cutome Action(method) must use action decorator
#"detail = False": this action available on LISTVIEW
#"detail = True": this action available on DETAILVIEW
    @action(detail= False, methods= ['GET', 'POST'], permission_classes= [IsAuthenticated])    
    def me(self, request):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED) 
               
        customer= Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serialier = CustomerSerializers(customer)
            return Response(serialier.data)
        elif request.method == 'POST':
            serialier = CustomerSerializers(customer, data= request.data)
            serialier.is_valid()
            serialier.save(raise_exception = True)
            return Response(serialier.data)
        
class OrderViewSets(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializers(
            data= request.data,
            context = {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception= True)
        order = serializer.save()
        serializer = OrderSerializers(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializers
        if self.request.method == 'PATCH':
            return UpdateOrderSerializers
        return OrderSerializers
        
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id= user.id)
        return Order.objects.filter(customer_id = customer_id)

class ProductImageViewSets(ModelViewSet):
    serializer_class = ProductImageSerializers
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['products_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['products_pk']}    