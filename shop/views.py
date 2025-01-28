from itertools import product
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from shop.models import Product, Order
from shop.forms import OrderForm


# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/index.html', context=context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    #product = Product.object.get(id=pk)

    return render(request, 'shop/detail.html', {'product': product})

def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form=OrderForm(request.GET)
        if form.is_valid():
            full_name = request.GET.get('full_name')
            phone_number = request.GET.get('phone_number')
            quantity = int(request.GET.get('quantity'))
            if product.quantity >= quantity:
                product.quantity -= quantity
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    message='Order successful sent'
                )
                order = Order.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=product
                )
                order.save()
                product.save()
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    message='Something with sent...'
                )


    else:
        form = OrderForm()
    connect = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', connect)
