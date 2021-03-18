from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm, CartUpdateProductForm
from records.models import Product, ProductParameter


# @require_POST
# def cart_add(request, product_id):
#     """ Добавление товаров в корзину """
#     cart = Cart(request)
#     print(cart)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('cart:cart_detail')


@require_POST
def cart_add(request):
    """ Добавление товаров в корзину """

    # if request.is_ajax():
    # получить id_info
    info_id = request.POST.get('info_id')
    # получить параметры, если они есть
    params_id = request.POST.getlist('params_id[]')
    # преобразовать полученные параметры в число
    params_id = set(map(int, params_id))
    product_id = None
    # получить все товары по info_id
    products = Product.objects.filter(product_info__id=info_id)

    # получить множество параметров по каждому параметру
    for product in products:
        product_parameters = set(ProductParameter.objects.filter(product=product)
                                 .values_list('parameter__id', flat=True).order_by('parameter__id'))
        # print("product_parameters", product_parameters)
        # если есть совпадение по товару, получить id
        if product_parameters == params_id:
            product_id = product.id

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        print('после? ', request.POST, '', form, 'cart', cart, form.is_valid())
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return HttpResponse("True")
    return HttpResponse("False")


def cart_remove(request, product_id):
    """ Удаление товаров из корзины """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """ Содержимое корзины """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartUpdateProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request,
                  'cart/detail.html',
                  {'cart': cart})


@require_POST
def cart_update(request, product_id):
    """ Обновление количества товаров в корзине """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, active=True, quantity__gt=0)
    form = CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print(product.quantity)
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')