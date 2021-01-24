import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Subquery, OuterRef, Exists
from django.shortcuts import render, get_object_or_404

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


""" Интернет-магазин """


@login_required
def shop(request, category_id=None):
    """ Главная страница интернет-магазина """
    section = 'shop'
    categories = Category.objects.filter(active=True)
    info_products = ProductInfo.objects.all()

    if category_id:
        info_products = ProductInfo.objects.filter(group_product__category=category_id)

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

    # Доступные параметры по артикулу
    vendor_code_parameters = Exists(ProductParameter.objects.filter(
        parameter=OuterRef('pk'),
        product__product_info__vendor_code=vendor_code))

    # все достпуные параметры группы
    all_parameters = Parameter.objects.filter(
        product_parameter_parameter__product__product_info__in=info_products) \
        .annotate(in_stock=vendor_code_parameters) \
        .order_by('parameter_id').distinct()

    cart_product_form = CartAddProductForm()

    return render(request,
                  'catalog/product/product_detail.html',
                  {'group_product': group_product,
                   'vendor_code': vendor_code,
                   'info_products': info_products,
                   'all_parameters': all_parameters,
                   'cart_product_form': cart_product_form,
                   'section': section})
