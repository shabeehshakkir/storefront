from django.shortcuts import render
from store.models import Product


def say_hello(request):
    query_set = Product.objects.all()  # QuerySet

    for product in query_set:  # Product
        print(product)

    return render(request, 'hello.html', {'name': 'Shabeeh'})
