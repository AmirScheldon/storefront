from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

# with using "ModelSerializer" we can quickly make serializer without duplication
class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'unit_price', 'inventory', 'collection', 'price_with_tax']
    price_with_tax = serializers.SerializerMethodField(method_name= 'tax_calculator')
    
    def tax_calculator(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    

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