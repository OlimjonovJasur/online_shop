from itertools import product
from lib2to3.fixes.fix_input import context
from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from shop.models import Product, Order, Category, Comment
from shop.forms import OrderForm, CommentModelForm, ProductModelForm


# Create your views here.
class IndexView(View):

    def get(self, request, category_id: Optional[int] = None, *args, **kwargs):
        search_query = request.GET.get('q', '')
        filter_type = request.GET.get('filter', '')
        categories = Category.objects.all()
        if category_id:
            if filter_type == 'expensive':
                products = Product.objects.filter(category_id=category_id).order_by('-price')
            elif filter_type == 'cheap':
                products = Product.objects.filter(category_id=category_id).order_by('price')
            elif filter_type == 'rating':
                products = Product.objects.filter(category_id=category_id, rating__gte=4).order_by('-rating')

            else:
                products = Product.objects.filter(category_id=category_id)

        else:
            if filter_type == 'expensive':
                products = Product.objects.all().order_by('-price')
            elif filter_type == 'cheap':
                products = Product.objects.all().order_by('price')
            elif filter_type == 'rating':
                products = Product.objects.filter(rating__gte=3).order_by('-rating')

            else:
                products = Product.objects.all()

        if search_query:
            products = Product.objects.filter(name__icontains=search_query)

        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, 'shop/index.html', context=context)

# def index(request, category_id: Optional[int] = None):
#     search_query = request.GET.get('q', '')
#     filter_type = request.GET.get('filter', '')
#     categories = Category.objects.all()
#     if category_id:
#         if filter_type == 'expensive':
#             products = Product.objects.filter(category_id=category_id).order_by('-price')
#         elif filter_type == 'cheap':
#             products = Product.objects.filter(category_id=category_id).order_by('price')
#         elif filter_type == 'rating':
#             products = Product.objects.filter(category_id=category_id, rating__gte=4).order_by('-rating')
#
#         else:
#             products = Product.objects.filter(category_id=category_id)
#
#     else:
#         if filter_type == 'expensive':
#             products = Product.objects.all().order_by('-price')
#         elif filter_type == 'cheap':
#             products = Product.objects.all().order_by('price')
#         elif filter_type == 'rating':
#             products = Product.objects.filter(rating__gte=3).order_by('-rating')
#
#         else:
#             products = Product.objects.all()
#
#     if search_query:
#         products = Product.objects.filter(name__icontains=search_query)
#
#
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#     return render(request, 'shop/index.html', context=context)

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = Comment.objects.filter(product=product, is_negative=False)
        related_products = Product.objects.filter(category_id=product.category).exclude(id=product.id)

        context = {
            'product': product,
            'comments': comments,
            'related_products': related_products
        }

        return render(request, 'shop/detail.html', context=context)

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     comments = Comment.objects.filter(product=product, is_negative=False)
#     related_products = Product.objects.filter(category_id=product.category).exclude(id=product.id)
#
#     context = {
#         'product': product,
#         'comments': comments,
#         'related_products': related_products
#     }
#
#     return render(request, 'shop/detail.html', context=context)

class OrderDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm(request.GET)
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





# def order_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         form=OrderForm(request.GET)
#         if form.is_valid():
#             full_name = request.GET.get('full_name')
#             phone_number = request.GET.get('phone_number')
#             quantity = int(request.GET.get('quantity'))
#             if product.quantity >= quantity:
#                 product.quantity -= quantity
#                 messages.add_message(
#                     request,
#                     messages.SUCCESS,
#                     message='Order successful sent'
#                 )
#                 order = Order.objects.create(
#                     full_name=full_name,
#                     phone_number=phone_number,
#                     quantity=quantity,
#                     product=product
#                 )
#                 order.save()
#                 product.save()
#             else:
#                 messages.add_message(
#                     request,
#                     messages.ERROR,
#                     message='Something with sent...'
#                 )
#
#
#     else:
#         form = OrderForm()
#     connect = {
#         'form': form,
#         'product': product
#     }
#
#     return render(request, 'shop/detail.html', connect)

class CommentView(View):
    def get(self, request, pk):
        product = CommentModelForm(Product, id=pk)
        form = CommentModelForm()
        context = {
            'product': product,
            'form': form,
        }
        return render(request, 'shop/detail.html', context=context)

    def post(self, request, pk):
        comment_form = CommentModelForm(data=request.POST)
        product = get_object_or_404(Product, id=pk)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment_form.product = product
            comment_form.save()
            return redirect('shop:product_detail', pk)
        else:
            return render(request, 'shop/detail.html', {'form': comment_form, 'product': product})




# def comment_view(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     form = CommentModelForm()
#     if request.method == 'POST':
#         form = CommentModelForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.product = product
#             comment.save()
#             return redirect('shop:product_detail', pk)
#     context = {
#         'product': product,
#         'form': form,
#     }
#     return render(request, 'shop/detail.html', context=context)




class ProductCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = ProductModelForm()
        context = {
            'form': form,
            'action': 'Create New'
        }
        return render(request, 'shop/create.html', context)

    def post(self, request, *args, **kwargs):
        form = ProductModelForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('shop:products')

        context = {
            'form': form,
            'action': 'Create New'
        }
        return render(request, 'shop/create.html', context)

# @login_required
# def product_create(request):
#     # form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('shop:products')
#     else:
#         form = ProductModelForm()
#     context = {
#         'form': form,
#         'action': 'Create New'
#     }
#     return render(request, 'shop/create.html', context=context)


class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return redirect('shop:products')

# def product_delete(request, pk):
#     try:
#         product = Product.objects.get(id=pk)
#         product.delete()
#         return redirect('shop:products')
#     except Product.DoesNotExists as e:
#         print(e)



class ProductEditView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductModelForm(instance=product)
        return render(request,'shop/create.html', {'form': form, 'action': 'Edit'})

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductModelForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', pk)

        else:
            return render(request, 'shop/create.html', {'form': form, 'action': 'Edit'  })


# def product_edit(request, pk):
#     product = Product.objects.get(id=pk)
#     form = ProductModelForm(instance=product)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('shop:product_detail', pk)
#     context = {
#         'form': form,
#         'product': product,
#         'action': 'Edit',
#     }
#
#     return render(request, 'shop/create.html', context=context)



