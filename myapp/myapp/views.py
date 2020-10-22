from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
# from order.models import Order


# def order_confirmation(request):
#     order = Order.objects.get(pk=45)
#
#     return render(request, 'order_confirmation.html', {'order': order})


def index(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(available=True)
    featured_products = Product.objects.filter(feature=True).filter(available=True)
    featured_categories = Category.objects.filter(feature=True)
    context = {
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
        'featured_categories': featured_categories,
        'title': 'index page'
    }

    return render(request, 'index.html', context)


def about(request):
    context = {
        'title': 'about page'
    }

    return render(request, 'about.html', context)


def contact(request):
    context = {
        'title': 'contact page'
    }

    return render(request, 'contact.html', context)


def reorder(request):
    context = {
        'title': 'reorder page'
    }

    return render(request, 'reorder.html', context)
