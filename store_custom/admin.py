from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInline(GenericTabularInline):
    extra = 0
    min_num = 1
    max_num = 5
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(ProductAdmin)
admin.site.register(Product, CustomProductAdmin)
# Register your models here.
