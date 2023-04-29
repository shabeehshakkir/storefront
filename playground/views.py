from django.shortcuts import render
from store.models import Product, Order, OrderItem, Customer
from django.db import transaction
from django.db.models import Value,DecimalField, F, ExpressionWrapper
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'hello.html', {'name': 'Shabeeh'})
