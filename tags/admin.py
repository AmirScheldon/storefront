from django.contrib import admin
from .models import Tag

# Register your models here.
 
@admin.register(Tag)
class NameAdmin(admin.ModelAdmin):
    search_fields = ['label']