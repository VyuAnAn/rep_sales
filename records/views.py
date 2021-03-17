import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Subquery, OuterRef, Exists
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from cart.forms import CartAddProductForm
from records.models import Category, SalesLogDetail, Product, GroupProduct, ProductInfo, Image, Parameter, \
    ProductParameter

""" Журнал продаж """
now = datetime.datetime.now()


@login_required
def sales_log(request, year=now.year, month=now.month, day=now.day):
    section = 'sales_log'
    logs = SalesLogDetail.objects.filter(sales_log__created__year=year,
                                         sales_log__created__month=month,
                                         sales_log__created__day=day)
    return render(request,
                  'sales_logs/sales_log.html',
                  {'logs': logs,
                   'section': section})

#
# @login_required
# def list_products(request, category_id=None):
#     section = 'sales_log'
#     categories = Category.active_categories.all()
#     info_products = ProductInfo.objects.all()
#
#     if category_id:
#         info_products = ProductInfo.objects.filter(group_product__category=category_id)
#
#     return render(request,
#                   'sales_log/list_products.html',
#                   {})


@login_required
def sell(request, product_id):
    section = 'sales_log'
    if request.method == 'POST':
        product = Product.obgects.get(id=product_id)
    else:
        pass
    return render(request,
                  'sales_logs/sell.html',
                  {'section': section
                   })


""" Интернет-магазин """


@login_required
def shop(request, category_id=None):
    """ Главная страница интернет-магазина """
    section = 'shop'
    categories = Category.objects.filter(active=True)
    info_products = ProductInfo.objects.all()

    # if category_id:
    #     info_products = ProductInfo.objects.filter(group_product__category=category_id)

    return render(request,
                  'catalog/product/index.html',
                  {'categories': categories,
                   'info_products': info_products,
                   'section': section})


@login_required
def product_detail(request, group_id, vendor_code):
    """ Информация по группе товаров"""
    section = 'shop'

    group_product = get_object_or_404(GroupProduct, id=group_id)
    info_products = ProductInfo.objects.filter(group_product=group_product)
    images = Image.objects.filter(product_info__vendor_code=vendor_code,
                                  main=False)
    info_product = get_object_or_404(ProductInfo, vendor_code=vendor_code)

    # Доступные параметры по артикулу
    vendor_code_parameters = Exists(ProductParameter.objects.filter(
        parameter=OuterRef('pk'),
        product__product_info__vendor_code=vendor_code))

    # все доступные параметры группы
    all_parameters = Parameter.objects.filter(
        product_parameter_parameter__product__product_info__in=info_products) \
        .annotate(in_stock=vendor_code_parameters) \
        .order_by('parameter_id', 'sort_number').distinct()

    cart_product_form = CartAddProductForm()

    return render(request,
                  'catalog/product/product_detail.html',
                  {'group_product': group_product,
                   'vendor_code': vendor_code,
                   'info_product': info_product,
                   'images': images,
                   'all_parameters': all_parameters,
                   'cart_product_form': cart_product_form,
                   'section': section})


# @login_required
# def get_product(request):
#     """ Получить id товара по параметрам """
#     if request.method == "POST" and request.is_ajax():
#         # получить id_info
#         info_id = request.POST.get('info_id')
#         # получить параметры, если они есть
#         params_id = request.POST.getlist('params_id[]')
#         # преобразовать полученные параметры в число
#         params_id = set(map(int, params_id))
#         product_id = None
#         # получить все товары по info_id
#         products = Product.objects.filter(product_info__id=info_id)
#
#         # получить множество параметров по каждому параметру
#         for product in products:
#             product_parameters = set(ProductParameter.objects.filter(product=product)
#                                      .values_list('parameter__id', flat=True).order_by('parameter__id'))
#             # print("product_parameters", product_parameters)
#             # если есть совпадение по товару, получить id
#             if product_parameters == params_id:
#                 product_id = product.id
#
#         # print("info_id: ", info_id, " params_id: ", params_id, "product_id", product_id)
#         return HttpResponseRedirect(reverse('cart:cart_add', args=(product_id,)))
#         # return HttpResponse(product_id)
#     return HttpResponse("fail")
