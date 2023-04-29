from django.contrib import admin, messages
from .models import Product, Order, OrderItem, Customer, Collection
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ['title']
                           }
    exclude = ['promotions']
    actions = ['clear_inventory']
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title', 'last_update')
    list_editable = ('unit_price',)
    list_per_page = 20
    list_filter = ('collection', 'last_update', InventoryFilter)
    list_select_related = ['collection']

    @admin.display(ordering='collection_title')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated', level='success')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership', 'orders_count',)
    list_editable = ('membership',)
    list_per_page = 20
    list_filter = ('membership',)
    search_fields = ('first_name__istartswith', 'last_name__istartswith',)

    # viewing customers orders
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = reverse('admin:store_order_changelist') \
              + '?' \
              + urlencode({
               'customer_id': str(customer.id)
        })

        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):    # this is to add the orders_count column to the admin page
        return super().get_queryset(request).annotate(
            orders_count=Count('order'))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ('id', 'placed_at', 'customer', 'payment_status')
    inlines = [OrderItemInline]
    list_per_page = 20
    list_filter = ('payment_status',)
    search_fields = ('product__title__istartswith',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    search_fields = ('title__istartswith',)

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') \
              + '?' \
              + urlencode({
               'collection__id': str(collection.id)
        })

        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product'))


admin.site.register(OrderItem)

# Register your models here.
