from django.shortcuts import render
from store.models import Product, Customer, Collection, Order, OrderItem


def say_hello(request):
    query_set = Product.objects.filter(unit_price__range=(20, 30))

    query_set_email = Customer.objects.filter(email__icontains='.com')  # .com

    query_set_featured = Collection.objects.filter(featured_product__isnull=True)

    query_set_product = Product.objects.filter(inventory__lt=10)

    query_set_order = Order.objects.filter(customer__id=1)

    query_set_product_id3 = OrderItem.objects.filter(order__id=3)

    return render(request, 'hello.html', {'name': 'Shabeeh', 'products': list(query_set),
                                          'customers': query_set_email,
                                          'not_featured': list(query_set_featured),
                                          'inventory': query_set_product,
                                          'order': list(query_set_order),
                                          'order_id3': list(query_set_product_id3)
                                          })
