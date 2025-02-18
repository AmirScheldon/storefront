from django.core.validators import MinValueValidator, FileExtensionValidator
from django.conf import settings
from django.contrib  import admin
from django.db import models
from uuid import uuid4
from .validator import validate_image_size

class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField()

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(null = True, blank = True)
    unit_price = models.DecimalField(
        max_digits= 5,
        decimal_places= 2,
        validators= [MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey('Collection', on_delete = models.PROTECT, related_name= 'products')
    promotions = models.ManyToManyField(Promotion, blank= True)       
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name = 'image')
    image = models.ImageField(upload_to= 'store/media',
                              validators= [FileExtensionValidator(allowed_extensions= ['jpg', 'png']), validate_image_size] )

class Collection(models.Model):
    name = models.CharField(max_length = 255)
    featured_product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, related_name = '+' )
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZE, 'Bronze') ]
    
    phone= models.CharField(max_length= 255)
    birth_date= models.DateField(null= True)
    membership = models.CharField(max_length= 1, choices = MEMBERSHIP_CHOICES, default= MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    
    @admin.display(ordering= 'user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering= 'user__last_name')    
    def last_name(self):
        return self.user.last_name
    
    def __str__(self) -> str:
        return f' {self.user.first_name} {self.user.last_name}'
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [('view_history', 'can see history') ]
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed')]
    
    placed_at = models.DateTimeField(auto_now_add= True)
    payment_status = models.CharField(max_length = 1, choices = PAYMENT_STATUS_CHOICES, default = PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT, related_name= 'customer')
    
    class Meta:
        permissions =[
            ('can_cancel', 'Can cancel order')
        ]
    
class Address(models.Model):
    zip =zip()
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, primary_key = True)

class OrderItem(models.Model):
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits = 6, decimal_places = 2)
    order = models.ForeignKey(Order, on_delete = models.PROTECT, related_name= 'items')
    product = models.ForeignKey( Product, on_delete = models.PROTECT, related_name= 'orderitems')

    

class Cart(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid4)
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1)]
    )
    class Meta:
        unique_together = [['product', 'cart']]
    
class Reviews(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.TextField()
    time = models.TimeField(auto_now_add=True)
