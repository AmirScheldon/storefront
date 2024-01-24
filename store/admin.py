from django.db.models import Count
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from store.models import Collection, Product, Customer, Order
from typing import Any
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


#override "SimpleListFilter"
class ProductInventory(admin.SimpleListFilter):
    title = 'Inventory'
    # we can see it in "query string" which we can se it on searchbar
    parameter_name = 'Inventory'
    
    # with this method we specify what item should be in "SimpleListFilter"
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
        #("filtering value", "human readable description")
            ('<10', 'Low')
        ]
    
    # we implement filtering logic in this method   
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Django ModelAdmin
    # exclude: you can customize all fields but the ones you listed 
    # fields: determine attributes you can write on
    # readonly_fields: determine readonly attributes
    # prepopulated_fields: {"field you want to populate": [field/fields that fill the KEY]}
    # autocomplete_fields: it doesn't make overhead. go to target class and define "search_fields"
    autocomplete_fields = ['collection']
    #implement overrides in 'action' button list
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'colllection_name']
    list_editable = ['unit_price']
    list_per_page = 10
    # if i don't use "list_select_related" and just use collection_name, django send extra querys to server.
    # "list_select_related" preload model.
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', ProductInventory]
    search_fields = ['product']
    
    def colllection_name(self, product):
        return product.collection.name
    
    @admin.display(ordering= 'unit_price')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    #to override "action button(on top left)"
    def clear_inventory(self, request, queryset):
        inventory_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{inventory_count} products were updated successfully',
            #to select type message (ERROR - WARNING - SUCCESS)
            messages.SUCCESS
        )

@admin.register(Customer)    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    # to search better use "lookup(__sth)"
    # i = insensitve
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ['first_name', 'last_name']
    
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
        
# TabularInline / StackedInline
# this class indirectly inheritate from ModelAdmin
class OrderItemInLine(admin.TabularInline):
    model = models.OrderItem
    # you should define "search_fields" in ProductAdmin
    autocomplete_fields = ['product']
    # define place holders 
    extra = 0
    # minimum and maximum number 
    min_num = 1
    max_num = 10   
    
@admin.register(Order)   
class OrderAdmin(admin.ModelAdmin):
    # in showing fields we dont see "placed_at" field bcz it autopopulate by django(auto_now_add= True). 
    fields = []
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    # define OrderItemInline to OrderAdmin
    inlines = [OrderItemInLine]

    
    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_counter']
    list_per_page = 10
    # it defines bcz of "autocomplete_fields" in ProductAdmin
    search_fields = ['name__istartswith']
    """
        we want link numbers in "product_counter" to product page(filter elements in this page too).
    """
    """
    we write html in 'format_html'. <a href = destination page></a> = link
    """
    @admin.display(ordering= 'product_counter')
    def product_counter(self, collection):
        #                      app_model_page
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

