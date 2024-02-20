from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from store.admin import ProductAdmin, Product, ProductImageInline
from tags.models import TaggedItem
from .models import User
# we make this app to independent "store" and "custom" of eachother
# by deleting name of application in INSTALLED_APP, "tags" will be deleted
 
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )

class TagInLine(GenericTabularInline):
    model = TaggedItem 
    autocomplete_fields = ['tag']
    
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine, ProductImageInline]
    
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)