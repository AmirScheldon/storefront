from django.db.models import Count
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from store.models import Collection, Product, Customer, Order
from typing import Any
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class ProductInventory(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'Inventory'
    

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
        #("filtering value", "human readable description")
            ('<10', 'Low')
        ]
      
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)   
        
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<image src= "{instance.image.url}" class = "thumbnail" />')
        return ''

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'colllection_name']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', ProductInventory]
    search_fields = ['product']
    inlines = [ProductImageInline]
    
    
    def colllection_name(self, product):
        return product.collection.name
    
    @admin.display(ordering= 'unit_price')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    def clear_inventory(self, request, queryset):
        inventory_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{inventory_count} products were updated successfully',
            messages.SUCCESS
        )
    class Media:
        css = {
            'all': ['store/style.css']
        }

@admin.register(Customer)    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ['user__first_name', 'user__last_name']
    
    @admin.display(ordering= 'orders')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
               )
        return format_html('<a href= {}>{}</a>', url, customer.orders)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders= Count('order')
        )
        
class OrderItemInLine(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10   
    
@admin.register(Order)   
class OrderAdmin(admin.ModelAdmin):
    fields = []
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    inlines = [OrderItemInLine]

    
    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_counter']
    list_per_page = 10
    search_fields = ['name__istartswith']
    
    @admin.display(ordering= 'product_counter')
    def product_counter(self, collection):
        url = (
                reverse('admin:store_product_changelist')
               + "?"
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html('<a href= {}>{}</a>', url, collection.product_counter)
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            product_counter = Count('products')
        )

