from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem, Customer, Order, OrderItem
from decimal import Decimal
from django.db import transaction
from .signals.signal import order_created

# with using "ModelSerializer" we can quickly make serializer without duplication
class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'products_count']
    products_count = serializers.IntegerField(read_only=True)
 
    
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'inventory', 'collection', 'price_with_tax']
    price_with_tax = serializers.SerializerMethodField(method_name= 'tax_calculator')
    
    def tax_calculator(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
class ReviewsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'name', 'description', 'time']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id = product_id , **validated_data)

class SimpleProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'unit_price']
    
class CartItemSerializers(serializers.ModelSerializer):
    product = SimpleProduct()
    product_total_price = serializers.SerializerMethodField()
    
    def get_product_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity
    
    def create(self, validated_data):
        items_id = self.context[items_id]
        return CartItem.object.create(items_id = items_id, **validated_data)
    
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'product_total_price']
        
    
class CartSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only= True)
    items = CartItemSerializers(many= True, read_only= True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        
class AddCartItemSerializers(serializers.ModelSerializer):
    product_id =serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No product does exist with given id was found.')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(product_id = product_id, cart_id= cart_id)
            cart_item.quantity += quantity 
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id , **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity'] 
        
class UpdateCartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        

class CustomerSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only= True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
        
class OrderItemSerializers(serializers.ModelSerializer):
    product = SimpleProduct()
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'product']
class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many= True)
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'placed_at', 'payment_status', 'items']
        
class UpdateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
        
class CreateOrderSerializers(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No cart with given id was found')
        if CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('Cart is empty')
        return cart_id    
    def save(self, **kwargs):
        with transaction.atomic():
            (customer, created) = Customer.objects.get_or_create(user_id = self.context['user_id'])
            order = Order.objects.create(customer = customer)
            
            cart_items = CartItem.objects.select_related('product').filter(cart_id = self._validated_data['cart_id'])
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    unit_price = item.product.unit_price,
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk = self._validated_data['cart_id']).delete()
            
            order_created.send_robust(self.__class__ , order = order)
            
            return order
        
        
"""
    serializing relationships:
        1.Primary key
        2.String
        3.Nested object
        4.Hyperlink
"""
# 3.Nested object
# class CollectionSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length= 255)
    
# # defining attribiutes is exactly looklike creating defining one in Modeling.
# class ProductSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length= 255)
#     # source= : name a attribute diffrently from what we have in root class( here Product)
#     price = serializers.DecimalField(max_digits= 6, decimal_places= 2, source= 'unit_price')
#     # creating a custom field 
#     price_with_tax = serializers.SerializerMethodField(method_name= 'tax_calculator')
#     # 1.Primary key
#     # collection_id = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all())
#     # 2.String
#     # this line make a lot of query that take us lots of time. to solve this go to store/views.py
#     # collection= serializers.StringRelatedField()
#     # 3.Nested object
#     # collection = CollectionSerializers()
#     # 4.Hyperlink
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name= "colllection_detail"
#     )

"""
    deserializing data: 
        *it happens when we receives data from client.
        * client send a POST request to an endpoint and it must be JSON!
        * on the server we have to read the data and deserialize it to store it in the database 
"""