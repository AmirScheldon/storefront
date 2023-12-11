from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.admin import ProductAdmin, Product
from tags.models import TaggedItem

# we make this app to independent "store" and "custom" of eachother
# by deleting name of application in INSTALLED_APP, "tags" will be deleted
 

class TagInLine(GenericTabularInline):
    model = TaggedItem 
    autocomplete_fields = ['tag']
    
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]
    
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)