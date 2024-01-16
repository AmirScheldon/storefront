from django.core.validators import MinValueValidator
from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField()
    #django makes a field named as Product_set. if you want change it, use 'related_name="sth" ' in Product!

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    # null = True: its for DB
    # blank = True: its for AdminPanel(validation purpose)
    description = models.TextField(null = True, blank = True)
    unit_price = models.DecimalField(
        max_digits= 5,
        decimal_places= 2,
        #it has default message that you can change it by "message="
        validators= [MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
    #if child came before parent, pass the STRING of parent!
    collection = models.ForeignKey('Collection', on_delete = models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank= True)       
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

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
    
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email=models.EmailField(max_length=254, unique= True)
    phone= models.CharField(max_length= 255)
    birth_date= models.DateField(null= True)
    membership = models.CharField(max_length= 1, choices = MEMBERSHIP_CHOICES, default= MEMBERSHIP_BRONZE)
    
    def __str__(self) -> str:
        return f' {self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name'] 
    
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
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
    
class Address(models.Model):
    zip =zip()
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, primary_key = True)

class OrderItem(models.Model):
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits = 6, decimal_places = 2)
    order = models.ForeignKey(Order, on_delete = models.PROTECT)
    # parent and child should be in order(parent define before child)
    product = models.ForeignKey( Product, on_delete = models.PROTECT)
    

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

